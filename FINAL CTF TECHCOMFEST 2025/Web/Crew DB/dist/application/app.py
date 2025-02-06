from flask import Flask, request, render_template
import pymysql
import re
import os

app = Flask(__name__)

DB_HOST = os.getenv("MYSQL_HOST")
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_NAME = os.getenv("MYSQL_DATABASE")

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def sanitize_input(input_value):
    patterns = [
        r"'", r'"', r"-", r"\d", r";", r",", r" ", r"	", r"OR", r"AND", r"FLAG",
        r"FALSE", r"TRUE" ,r"UNION", r"ORDER", r"SELECT", r"FROM", 
    ]
    for pattern in patterns:
        input_value = re.sub(pattern, "", input_value, flags=re.IGNORECASE)
        print(input_value)
    print(f"Input value: {input_value}")
    return input_value

@app.route("/", methods=["GET", "POST"])
def index():
    role = ""
    expertise = ""
    data = []
    all_records = []

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            if request.method == "POST":
                sanitized_role = sanitize_input(request.form.get("role", ""))
                sanitized_expertise = sanitize_input(request.form.get("expertise", ""))

                query = f"SELECT * FROM cyber_heist_crew WHERE role = '{sanitized_role}' AND expertise = '{sanitized_expertise}'"
                cursor.execute(query)
                data = cursor.fetchall()

            cursor.execute("SELECT * FROM cyber_heist_crew")
            all_records = cursor.fetchall()

    except Exception as e:
        data = f"Error: {str(e)}"
    finally:
        conn.close()

    return render_template("index.html", data=data, all_records=all_records)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337, debug=False)
