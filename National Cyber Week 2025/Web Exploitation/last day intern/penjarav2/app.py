import builtins
import unicodedata
from flask import Flask, render_template, request, redirect, url_for, session, g, flash, abort
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from urllib.parse import urlparse
import ipaddress, socket 
import time


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "instance", "users.sqlite")

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
app.config["DATABASE"] = DB_PATH


def get_db():
    if "db" not in g:
        os.makedirs(os.path.dirname(app.config["DATABASE"]), exist_ok=True)
        g.db = sqlite3.connect(app.config["DATABASE"], check_same_thread=False)
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    db = get_db()
    db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    );
    """)
    db.commit()

@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


with app.app_context():
    init_db()


def is_http_url(u: str) -> bool:
    try:
        p = urlparse(u)
        return p.scheme in ("http", "https") and p.netloc != ""
    except Exception:
        return False

def current_user():
    if "user_id" not in session:
        return None
    db = get_db()
    cur = db.execute("SELECT id, username, role FROM users WHERE id = ?", (session["user_id"],))
    return cur.fetchone()


@app.route("/")
def index():
    return render_template("index.html", user=current_user())

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Username and password required", "danger")
            return redirect(url_for("register"))
        db = get_db()
        hashed = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed, "user"))
            db.commit()
            flash("Registered. Please log in.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash("Username already exists or error", "danger")
            return redirect(url_for("register"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        db = get_db()
        cur = db.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row and check_password_hash(row["password"], password):
            session["user_id"] = row["id"]
            flash("Logged in", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=user)

@app.route("/fetch", methods=["GET", "POST"])
def fetch():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    result = None
    error = None
    if request.method == "POST":
        target = request.form.get("target", "").strip()
        if not is_http_url(target):
            error = "Invalid URL"
        elif is_private_url(target):
            error = "Private/internal URL not allowed"
        else:
            try:
                time.sleep(1)
                resp = requests.get(target, timeout=5)
                result = {
                    "status_code": resp.status_code,
                    "text": resp.text
                }
            except Exception as e:
                error = f"Fetch error: {e}"
    return render_template("fetch.html", user=user, result=result, error=error)

@app.route("/admin_internal")
def admin_internal():
     if request.remote_addr != '127.0.0.1':
        return "Access denied", 403
     
     name = request.args.get("name", "")
     output = None
     error = None
     normalized = unicodedata.normalize("NFKC", name)

     if any(ord(ch) > 127 for ch in normalized):
        return "no weird unicode allowed", 400
     blacklist = [
        "__import__",
        "__builtins__",
        "sh",
        "os",
        "popen",
        "system",
        "sh",
        "'",   
        '"',   
        "_",
        "open",   
     ]

     lowered = normalized.lower()
     for word in blacklist:
        if word in lowered:   
            return f"nuh uh {word}", 400
     try:
        wow = normalized
        result = eval(wow, {"__builtins__": builtins}, {})
        output = repr(result)
     except Exception as e:
        error = str(e)

     return render_template(
     "admin_internal.html",
      user=current_user(),
      payload=name,
      output=output,
      error=error,
)

def is_private_url(url):
    try:
        hostname = urlparse(url).hostname
        ip = ipaddress.ip_address(socket.gethostbyname(hostname))
        return ip.is_private
    except:
        return True

@app.route("/secret")
def secret():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    return render_template("secret.html", user=user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

