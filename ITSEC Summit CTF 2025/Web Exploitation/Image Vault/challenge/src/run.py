import time, threading
import os

from application.app import app
from application.util.database import Database

def start_server():
    app.run(host="0.0.0.0", port=1337, threaded=True, debug=False, ssl_context=('ssl/cert.pem', 'ssl/key.pem'))

if __name__ == "__main__":
    db = Database(app)

    db.migrate("admin", os.getenv("ADMIN_PASSWORD"), "admin@admin.com", "admin")

    start_server()