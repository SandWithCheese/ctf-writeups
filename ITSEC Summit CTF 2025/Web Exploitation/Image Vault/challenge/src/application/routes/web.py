import os
from application.util.database import Database
from flask import Blueprint, request, jsonify, render_template, session, redirect
from functools import wraps

web_blueprint = Blueprint("web", __name__)
db = Database()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("is_loggedin") != True and session.get("username") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            return redirect("/home")
        return f(*args, **kwargs)
    return decorated_function


@web_blueprint.get("/")
def index():
    return render_template("index.html")

@web_blueprint.get("/login")
def login():
    if  session.get("username") is not None:
        return redirect("/home")

    return render_template("login.html")

@web_blueprint.get("/register")
def register():
    if session.get("username") is not None:
        return redirect("/home")

    return render_template("register.html")

@web_blueprint.get("/home")
@login_required
def home():
    images = db.list_image(session.get("username"))
    return render_template("home.html", images=images)

@web_blueprint.get("/upload")
@login_required
def upload():
    return render_template("upload.html")

@web_blueprint.get("/invite")
@login_required
@is_admin
def invite():
    invited = db.list_invitation()
    return render_template("invite.html", invited=invited)

@web_blueprint.get("/flag")
@login_required
@is_admin
def flag():
    flag = os.environ.get('FLAG')
    return render_template("flag.html", flag=flag)

@web_blueprint.get("/report")
def report():
    return render_template("report.html")