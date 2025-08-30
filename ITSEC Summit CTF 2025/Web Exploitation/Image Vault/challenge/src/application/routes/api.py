import os
import threading
from application.util.database import Database
from application.util.bot import visit_url, active_visits
from base64 import b64decode
from cmagick import cmagick
from flask import Blueprint, request, jsonify, session, redirect, current_app
from flask_cors import CORS, cross_origin
from functools import wraps
from uuid import uuid4

api_blueprint = Blueprint("api", __name__)
db = Database()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("is_loggedin") != True and session.get("username") is None:
            return jsonify({"success":False, "message": "You must logged in first"}), 401
        return f(*args, **kwargs)
    return decorated_function

def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            return jsonify({"success":False, "message": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

def format_json(placeholder, data, exclude=[]):
    def to_dict(obj):
        return {
            k: v for k, v in obj.__dict__.items()
            if not k.startswith('_') and k not in exclude
        }

    if data is None:
        return {placeholder: None}

    elif isinstance(data, list):
        return {placeholder: [to_dict(obj) for obj in data]}
        
    else:
        return {placeholder: to_dict(data)}


@api_blueprint.post("/login")
@cross_origin(origins="*", supports_credentials=True)
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = db.login(username, password)
    
    if not user:
        return jsonify({"success":False, "message": "Invalid credentials"}), 401

    session["username"] = user.username
    session["role"] = user.role
    session["is_loggedin"] = True

    return jsonify({"success":True, "message": "Login successful"}), 200

@api_blueprint.post("/register")
@cross_origin(origins="*", supports_credentials=True)
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    invite_code = data.get("invite_code")

    status, user = db.register(username, password, email, "user", invite_code)
    
    if not status:
        return jsonify({"success": False, "message": user}), 400

    session["username"] = user.username
    session["role"] = user.role
    session["is_loggedin"] = True

    return jsonify({"success": True, "message": "Invite code successfully created"}), 200

@api_blueprint.get("/invite-code/<username>")
@cross_origin(origins="*", supports_credentials=True)
@login_required
@is_admin
def view_invite_code(username): 
    return jsonify(format_json("invite_code", db.list_invitation(username))), 200

@api_blueprint.post("/add-invite-code")
@login_required
@is_admin
def add_invite_code():
    data = request.get_json(force=True)
    username = data.get("username")

    if not username or username is None:
        return jsonify({"success": False, "message": "Bad Request"}), 400

    status, invitation = db.create_invitation(username)
  
    if not status:
        return jsonify({"success": False, "message": invitation}), 400

    return jsonify({"success": True, "message": invitation}), 200
    
@api_blueprint.post("/upload")
@cross_origin(origins="*", supports_credentials=True)
@login_required
def upload():
    data = request.get_json()
    base64_image = data.get("image")
    filename = f"{uuid4()}.png"
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    
    if not base64_image or base64_image is None:
        return jsonify({"success": False, "message": "Bad Request"}), 400

    try:
        image = b64decode(base64_image)
        with open(file_path, "wb") as f:
            f.write(image)
        
        cmagick.resize(file_path, "75%", file_path)
        db.add_image(session.get("username"), filename)

    except:
        return jsonify({"success": False, "message": "Bad Request"}), 400

    return jsonify({"success": True}), 200

@api_blueprint.post("/report")
@cross_origin(origins="*", supports_credentials=True)
def report_broken_link():
    data = request.get_json()
    url = data.get("url")
    ip = request.remote_addr

    if ip in active_visits:
        return jsonify({"success": False, "message": "Bot is already processing a URL for your IP. Please wait until it finishes."}), 429

    
    if not url or not (url.startswith("https://localhost:1337") or url.startswith("https://127.0.0.1:1337")):
        return jsonify({"success": False, "message": "Invalid URL."}), 400

    active_visits.add(ip)
    
    threading.Thread(target=visit_url, args=(url, ip), daemon=True).start()
    return jsonify({"success": True, "message": "Bot is visiting your URL."})