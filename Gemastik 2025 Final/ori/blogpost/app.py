import os
import sqlite3
from flask import (
    Flask, g, request, session, redirect, url_for,
    render_template, render_template_string, flash, abort, send_from_directory
)
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import re
from markupsafe import escape as m_escape

APP_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_DIR, "uploads")
DB_PATH = "/data/app.db"
FLAG_PATH = "/app/flag.txt"

ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'bmp'}

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH, check_same_thread=False)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password:
            flash("Missing username or password")
            return redirect(url_for("register"))
        hashed = generate_password_hash(password)
        db = get_db()
        try:
            db.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed, "user"))
            db.commit()
            flash("Registered. Please login.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already taken")
            return redirect(url_for("register"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        db = get_db()
        cur = db.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row and check_password_hash(row["password"], password):
            session["user_id"] = row["id"]
            session["username"] = row["username"]
            session["role"] = row["role"]
            flash("Logged in")
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out")
    return redirect(url_for("index"))

@app.route("/", methods=["GET", "POST"])
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    db = get_db()
    q = request.values.get("q", "").strip()

    if q:
        cur = db.execute(
            "SELECT p.*, u.username AS author "
            "FROM posts p LEFT JOIN users u ON p.author_id = u.id "
            "WHERE p.author_id = ? AND (p.title LIKE ? OR p.content LIKE ?) "
            "ORDER BY p.id DESC",
            (user_id, f"%{q}%", f"%{q}%")
        )
    else:
        cur = db.execute(
            "SELECT p.*, u.username AS author "
            "FROM posts p LEFT JOIN users u ON p.author_id = u.id "
            "WHERE p.author_id = ? "
            "ORDER BY p.id DESC",
            (user_id,)
        )

    posts = cur.fetchall()
    return render_template("index.html", posts=posts, q=q)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

@app.route("/create", methods=["GET", "POST"])
def create_post():
    if "user_id" not in session:
        flash("Login required")
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")
        file = request.files.get("image")
        image_filename = None
        metadata_text = ""
        if file and allowed_file(file.filename):
            original_filename = file.filename
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(save_path)

            try:
                cmd = f"exiftool {save_path}"
                meta_file = save_path + ".meta"
                full_cmd = f"{cmd} > {meta_file} 2>&1"
                os_status = os.system(full_cmd)
                if os.path.exists(meta_file):
                    with open(meta_file, "r", encoding="utf-8", errors="ignore") as mf:
                        metadata_text = mf.read()
                else:
                    metadata_text = "no-metadata"
            except Exception as e:
                metadata_text = f"exif_err: {e}"

            try:
                h = hashlib.sha256()
                with open(save_path, "rb") as fbin:
                    for chunk in iter(lambda: fbin.read(8192), b""):
                        h.update(chunk)
                digest = h.hexdigest()
                _, ext = os.path.splitext(original_filename)
                ext = ext.lower() if ext else ""
                new_filename = f"{digest}{ext}"
                new_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                new_meta = new_path + ".meta"

                if not os.path.exists(new_path):
                    os.replace(save_path, new_path)
                else:
                    try:
                        os.remove(save_path)
                    except Exception:
                        pass

                if os.path.exists(meta_file):
                    try:
                        os.replace(meta_file, new_meta)
                    except Exception:
                        try:
                            with open(meta_file, "rb") as mf_src, open(new_meta, "wb") as mf_dst:
                                mf_dst.write(mf_src.read())
                            os.remove(meta_file)
                        except Exception:
                            pass

                image_filename = new_filename
                if os.path.exists(new_meta):
                    try:
                        with open(new_meta, "r", encoding="utf-8", errors="ignore") as mf2:
                            metadata_text = mf2.read()
                    except Exception:
                        pass
            except Exception as e:
                image_filename = original_filename

            db = get_db()
            try:
                cur = db.execute(
                    "INSERT INTO posts (title, content, image_filename, author_id) VALUES (?, ?, ?, ?)",
                    (title, content, image_filename, session['user_id'])
                )
                db.commit()
                post_id = cur.lastrowid
                metadata_insert = f"UPDATE posts SET metadata = '{metadata_text}' WHERE id = {post_id};"
                db.executescript(metadata_insert)
                db.commit()
            except Exception as e:
                db.execute(
                    "UPDATE posts SET metadata = ? WHERE id = ?",
                    (metadata_text, post_id if 'post_id' in locals() else None)
                )
                db.commit()
            flash("Post created")
            return redirect(url_for("index"))
        else:
            flash("Missing or invalid image (png/jpg/jpeg/bmp)")
    return render_template("create_post.html")

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    if "user_id" not in session:
        return redirect(url_for("login"))
    if ".." in filename or filename.startswith("/"):
        abort(404)
    db = get_db()
    cur = db.execute("SELECT id FROM posts WHERE image_filename = ? AND author_id = ?", (filename, session["user_id"]))
    row = cur.fetchone()
    if not row:
        abort(404)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/post/<int:pid>")
def view_post(pid):
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    cur = db.execute(
        "SELECT p.*, u.username as author FROM posts p LEFT JOIN users u ON p.author_id = u.id WHERE p.id = ? AND p.author_id = ?",
        (pid, session["user_id"])
    )
    post = cur.fetchone()
    if not post:
        abort(404)
    return render_template("view_post.html", post=post)

@app.route("/profile")
def profile():
    if "user_id" not in session:
        flash("Login required")
        return redirect(url_for("login"))
    db = get_db()
    cur = db.execute("SELECT id, username, role FROM users WHERE id = ?", (session["user_id"],))
    user = cur.fetchone()
    flag_content = None

    with open(os.path.join(APP_DIR, "templates", "profile.html"), "r", encoding="utf-8") as fh:
        profile_template = fh.read()

    username = user["username"] if user else ""
    profile_source = profile_template.replace("{{ user.username }}", username)

    if user and user["role"] == "admin":
        try:
            with open(FLAG_PATH, "r") as f:
                flag_content = f.read().strip()
        except Exception:
            flag_content = "flag not found"
    return render_template_string(profile_source, user=user, flag=flag_content)

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host="0.0.0.0", port=8000)
