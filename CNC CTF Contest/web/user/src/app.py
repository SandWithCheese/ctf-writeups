import sqlite3

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
db_file = "usernames.db"

@app.route("/")
def index():
    users = get_users()
    return render_template("index.html", users=users)

# Function to create the 'users' table if it doesn't exist
def create_users_table():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flag (
          id INTEGER PRIMARY KEY,
          value TEXT NOT NULL
        );
    """)
    cursor.execute("""
        INSERT INTO flag (value) VALUES ('REDACTED');
    """)
    conn.commit()
    conn.close()

@app.route("/add_user", methods=["POST"])
def add_user():
    try:
        username = request.form["username"]  # Retrieve username from form data
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        conn.close()
        users = get_users()        
        return render_template("index.html", users=users)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/get_users", methods=["GET"])
def get_users():
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users")
        users = [row[0] for row in cursor.fetchall()]
        conn.close()
        return users
    except Exception as e:
        return str(e)

@app.route("/search_user", methods=["GET"])
def search_user():
    try:
        query = request.args.get("query")
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username like '%" + query + "%'")
        users = [row[0] for row in cursor.fetchall()]
        conn.close()
        return render_template("index.html", users=users)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    create_users_table()
    app.run(debug=True)