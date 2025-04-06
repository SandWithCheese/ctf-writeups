from flask import Flask, request, render_template_string, jsonify, redirect, url_for, make_response
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import uuid
import secrets
import string
import jwt
import datetime
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
app.config['PREFERRED_URL_SCHEME'] = 'http'
app.config['SERVER_NAME'] = 'localhost:7000'

FEEDBACK_DIR = "./feedback/"
os.makedirs(FEEDBACK_DIR, exist_ok=True)

my_secret = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(18))
VALID_CREDENTIALS = {
    'username': 'belugainfo',
    'password': my_secret
}

SECRET_KEY = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(20))
def generated_token():
    token = jwt.encode({'username': VALID_CREDENTIALS['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except ExpiredSignatureError:
        return False
    except InvalidTokenError:
        return False

@app.route("/")
def index():
    return open("template/login.html").read()

@app.route("/send", methods=["GET"])
def user_dashboard():
    token = request.cookies.get('auth_token')
    if not token or not verify_token(token):
        return "Unauthorized access! Please log in first", 401
    return open("template/index.html").read()

@app.route("/send-feedback", methods=["POST"])
def send_feedback():

    PROTECTED = ["." , "x", "{{", "]", "}}", "_", "[", "\\",]

    feedback = request.form.get("feedback", "")
    if not feedback:
        return "Feedback cannot be empty!", 400
    
    if any(word in feedback for word in PROTECTED):
        return "Feedback contains invalid characters!", 400
    else:
        random_id = str(uuid.uuid4())
        rendered_feedback = render_template_string(f"Admin received: {feedback}")
        
        feedback_file = os.path.join(FEEDBACK_DIR, f"{random_id}.txt")
        with open(feedback_file, "w") as f:
            f.write(rendered_feedback)

    return jsonify({"message": "Feedback sent!", "feedback_id": random_id})


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        secret_query = f"cn={username}||password={password}"

        if (username == VALID_CREDENTIALS['username'] and password == VALID_CREDENTIALS['password']) or any(char in secret_query for char in ['*', '(', ')', '\\']):
            token = generated_token()
            response = make_response(redirect(url_for('user_dashboard')))
            response.set_cookie('auth_token', token)
            return response
        else:
            return "Invalid credentials!", 401

@app.route("/api/private/feedback/<feedback_id>.txt")
def get_feedback(feedback_id):
    feedback_file = os.path.join(FEEDBACK_DIR, f"{feedback_id}.txt")
    if os.path.exists(feedback_file):
        return open(feedback_file).read(), 200
    return "Feedback not found", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

