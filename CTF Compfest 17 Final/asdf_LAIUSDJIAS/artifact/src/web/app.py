from flask import Flask, render_template, request, jsonify, Response, redirect
from subprocess import run
import yaml
import re
import os
import uuid
import json
from lxml import etree
from db import init_db, save_message, get_message, db_capture_webhook, db_view_webhook

app = Flask(__name__)

init_db()


# Main Routing
@app.route("/")
def index():
    return redirect("/web")


# Catch-all route → redirect to /public
@app.route("/<path:subpath>")
def catch_all(subpath):
    return redirect("/web")


@app.route("/web", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/web/admin", methods=["GET"])
def admin():
    if request.cookies.get("admin-key") != os.getenv("ADMIN_KEY", "secret"):
        return "Access Denied", 403
    return render_template("admin.html")


@app.route("/web/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")

    inner = request.form.get("data", "")

    try:
        if "xi:include" in inner or "http://www.w3.org/2001/XInclude" in inner:
            return Response("XInclude not permitted in user input", status=400)
        xml_data = f"<data><feedback>{inner}</feedback></data>"
        parser = etree.XMLParser(resolve_entities=False)
        root = etree.fromstring(xml_data.encode("utf-8"), parser=parser)
        tree = etree.ElementTree(root)
        tree.xinclude()

        feedback_elem = root.find("feedback")
        feedback = feedback_elem.text if feedback_elem is not None else ""

        contact_id = str(uuid.uuid4())
        save_message(contact_id, feedback)

        return render_template("contact_success.html", contact_id=contact_id)
    except Exception as exc:
        return Response(str(exc), status=400)


@app.route("/web/contact/<contact_id>", methods=["GET"])
def contact_view(contact_id):
    feedback = get_message(contact_id)
    if feedback is None:
        return "Contact not found", 404
    return render_template(
        "contact_view.html", contact_id=contact_id, feedback=feedback
    )


@app.route("/web/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        url = request.form.get("url", "")
        if not url:
            return jsonify({"error": "Url is missing."}), 400
        if not re.match(r"^https?://", url):
            return (
                jsonify({"error": "URL didn't match this regex format ^https?://"}),
                422,
            )
        else:
            result = run(["node", "/app/bot/bot.js", url], shell=False)
            if result.returncode == 0:
                return jsonify({"success": "Admin successfully visited the URL."})
            else:
                return jsonify({"error": "Admin failed to visit the URL."}), 500
    return render_template("report.html")


# AnD no outbound connection :(
@app.route("/webhook/capture/<id>")
def webhook_capture(id):
    try:
        uuid.UUID(id)
    except ValueError:
        return jsonify({"error": "Invalid UUID"}), 400
    method = request.method
    url = request.url
    if request.is_json:
        body = json.dumps(request.get_json())
    else:
        body = request.get_data(as_text=True)
    headers = dict(request.headers)
    db_capture_webhook(method, id, url, body, headers)
    return jsonify({"success": "request captured"}), 200


@app.route("/webhook/view/<id>", methods=["GET"])
def webhook_view(id):
    try:
        uuid.UUID(id)
    except ValueError:
        return jsonify({"error": "Invalid UUID"}), 400
    data = db_view_webhook(id)
    if data is None:
        return jsonify({"error": "No webhook data found"}), 404
    return jsonify(data), 200


# Additional features


@app.route('/web/guess', methods=['GET'])
def guess():
    q_raw = request.args.get("q", "").strip()
    # Accept only 1-3 digits and coerce to a bounded integer 1..100
    if re.fullmatch(r'\d{1,3}', q_raw):
        q_int = int(q_raw)
        if 1 <= q_int <= 100:
            q = str(q_int)
        else:
            q = ""
    else:
        q = ""

    return render_template("guess.html", value=q)


@app.route("/web/yaml", methods=["POST"])
def yaml_parser():
    if request.cookies.get("admin-key") != os.getenv("ADMIN_KEY", "secret"):
        return "Access Denied", 403
    yaml_data = request.form.get("yaml_data", "")
    if re.search(r"[()*_]", yaml_data):
        result = "Invalid characters in input"
    else:
        try:
            result = yaml.load(yaml_data, Loader=yaml.Loader)
            if result is None:
                result = "Empty YAML or null result"
            else:
                result = str(result)
        except Exception as e:
            result = str(e)
    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
