import os
import re
import sqlite3
import hashlib
import secrets
import datetime
import subprocess
from pathlib import Path
from functools import wraps

from flask import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "data.db")
UPLOAD_DIR = os.path.join(APP_DIR, "uploads")

ALLOWED_EXT = {"png", "jpg", "jpeg", "bmp"}
MAX_CONTENT_LENGTH = 8 * 1024 * 1024

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(16))
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.config["UPLOAD_FOLDER"] = UPLOAD_DIR

def get_db():
    db = getattr(g, "_db", None)
    if db is None:
        db = g._db = sqlite3.connect(DB_PATH, check_same_thread=False)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_db(_exc):
    db = getattr(g, "_db", None)
    if db:
        db.close()

def init_db():
    Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    db = get_db()
    db.executescript(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user',
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        filename TEXT NOT NULL,
        metadata TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );

    CREATE INDEX IF NOT EXISTS idx_posts_user_file ON posts(user_id, filename);
    """
    )
    db.commit()

def current_user():
    if "uid" not in session:
        return None
    db = get_db()
    cur = db.execute("SELECT id, username, role FROM users WHERE id = ?", (session["uid"],))
    return cur.fetchone()

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            dest = request.path
            flash("Please log in to continue.")
            return redirect(url_for("login", next=dest))
        return view(*args, **kwargs)
    return wrapped

def _is_within(child_path: str, parent_dir: str) -> bool:
    child_real = os.path.realpath(child_path)
    parent_real = os.path.realpath(parent_dir)
    try:
        return os.path.commonpath([child_real, parent_real]) == parent_real
    except ValueError:
        return False

def _exiftool_text(path_on_disk: str) -> str:
    if not _is_within(path_on_disk, UPLOAD_DIR):
        return "no-metadata"
    try:
        proc = subprocess.run(
            ["exiftool", "--", path_on_disk],
            capture_output=True,
            text=True,
            timeout=5
        )
        if proc.returncode != 0:
            return "no-metadata"
        return proc.stdout if proc.stdout else "no-metadata"
    except subprocess.TimeoutExpired:
        return "exif_err: timeout"
    except FileNotFoundError:
        return "exif_err: exiftool not found"
    except Exception as e:
        return f"exif_err: {e}"

def allowed_file(fn: str) -> bool:
    if "." not in fn:
        return False
    ext = fn.rsplit(".", 1)[-1].lower()
    return ext in ALLOWED_EXT

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Username and password required")
            return render_template("register.html")
        pw_hash = generate_password_hash(password)
        try:
            db = get_db()
            db.execute(
                "INSERT INTO users (username, password_hash, role, created_at) VALUES (?, ?, 'user', ?)",
                (username, pw_hash, datetime.datetime.utcnow().isoformat() + "Z"),
            )
            db.commit()
        except sqlite3.IntegrityError:
            flash("Username already exists")
            return render_template("register.html")
        flash("Registered. Please login.")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        db = get_db()
        cur = db.execute(
            "SELECT id, username, password_hash, role FROM users WHERE username = ?",
            (username,),
        )
        row = cur.fetchone()
        if not row or not check_password_hash(row["password_hash"], password):
            flash("Invalid credentials")
            return render_template("login.html")

        session["uid"] = row["id"]
        flash(f"Welcome, {row['username']}!")

        next_url = request.args.get("next") or request.form.get("next")
        if next_url and next_url.startswith("/"):
            return redirect(next_url)
        return redirect(url_for("gallery"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out")
    return redirect(url_for("login"))

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    user = current_user()
    if request.method == "POST":
        title = request.form.get("title", "").strip() or "(untitled)"
        f = request.files.get("image")
        if not f or f.filename == "":
            flash("Choose an image.")
            return render_template("upload.html")
        orig_name = secure_filename(f.filename)
        if not allowed_file(orig_name):
            flash("Unsupported file type.")
            return render_template("upload.html")
        ext = orig_name.rsplit(".", 1)[-1].lower()
        data = f.read()
        sha = sha256_hex(data)
        stored = f"{sha}.{ext}"
        path = Path(UPLOAD_DIR) / stored
        if not path.exists():
            path.write_bytes(data)
        metadata_blob = _exiftool_text(str(path))
        db = get_db()
        db.execute(
            """
            INSERT INTO posts (user_id, title, filename, metadata, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user["id"], title, stored, metadata_blob, datetime.datetime.utcnow().isoformat() + "Z"),
        )
        db.commit()
        flash("Upload complete.")
        return redirect(url_for("gallery"))
    return render_template("upload.html")

@app.route("/")
@app.route("/gallery")
@login_required
def gallery():
    user = current_user()
    db = get_db()
    cur = db.execute(
        """
        SELECT p.id, p.title, p.filename, p.created_at, u.username
        FROM posts p JOIN users u ON p.user_id = u.id
        WHERE p.user_id = ?
        ORDER BY p.id DESC
        """,
        (user["id"],),
    )
    posts = cur.fetchall()
    return render_template("gallery.html", posts=posts, user=user)

@app.route("/post/<int:pid>")
@login_required
def view_post(pid):
    user = current_user()
    db = get_db()
    cur = db.execute(
        "SELECT p.*, u.username FROM posts p JOIN users u ON p.user_id = u.id WHERE p.id = ? AND p.user_id = ?",
        (pid, user["id"]),
    )
    post = cur.fetchone()
    if not post:
        abort(404)
    if request.args.get("meta") == "1":
        return Response((post["metadata"] or ""), mimetype="text/plain")
    metadata_full = post["metadata"] or ""
    md_map = {"File Name": "", "Date Created": ""}
    for m in re.finditer(r"^\s*(File Name|Date Created)\s*:\s*(.*)$", metadata_full, flags=re.MULTILINE):
        key = m.group(1)
        val = m.group(2).strip()
        md_map[key] = val
    file_name_val = md_map["File Name"]
    date_created_val = md_map["Date Created"]
    metadata_snippet_html = f"<pre>File Name: {file_name_val}\nDate Created: {date_created_val}</pre>"
    tpl_path = os.path.join(APP_DIR, "templates", "view_post.html")
    with open(tpl_path, "r", encoding="utf-8") as fh:
        tpl_src = fh.read()
    placeholder = "{{ metadata_snippet or '' }}"
    if placeholder not in tpl_src:
        page_src = tpl_src + "\n" + metadata_snippet_html
    else:
        page_src = tpl_src.replace(placeholder, metadata_snippet_html)
    return render_template_string(page_src, post=post)

@app.route("/i/<path:filename>")
@login_required
def cdn_serve(filename):
    user = current_user()
    db = get_db()
    cur = db.execute(
        "SELECT 1 FROM posts WHERE user_id = ? AND filename = ? LIMIT 1",
        (user["id"], filename),
    )
    if not cur.fetchone():
        abort(404)  

    resp = send_from_directory(UPLOAD_DIR, filename, as_attachment=False)
    resp.headers["Cache-Control"] = "private, max-age=0, no-store"
    return resp

@app.errorhandler(413)
def too_large(_):
    flash("File too large.")
    return redirect(url_for("upload"))

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", port=8000, debug=False)
