from flask import Flask, request, jsonify, make_response
import sqlite3
from base64 import b64encode
import os
import uuid

app = Flask(__name__)
flag_value = os.environ.get('FLAG') or 'FLAG{test_flag}'
secret_value = str(uuid.uuid4())

if not os.path.exists('database.db'):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    conn.commit()
    conn.close()

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM users WHERE username=?', (os.environ.get('ADMIN_USERNAME') or 'testing',))
if cursor.fetchone() is None:
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (os.environ.get('ADMIN_USERNAME') or 'testing', os.environ.get('ADMIN_PASSWORD') or 'testing'))
    conn.commit()
conn.close()

@app.route('/')
def index():
    if request.remote_addr != '127.0.0.1':
        return "Not accessible through internet"

    return "Hello admin!"

@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    if username is None or password is None:
        return 'invalid', 403

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM users WHERE username="{username}" AND password="{password}"')
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return 'invalid', 403

    response = make_response(secret_value)
    response.set_cookie('session', secret_value)
    return response

@app.route('/flag')
def flag():
    if request.remote_addr != '127.0.0.1' or 'secret' not in request.args or request.args.get('secret') != secret_value:
        return 'invalid', 403

    encoded_flag = b64encode(flag_value.encode()).decode()
    return encoded_flag

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='127.0.0.1', port=5001)