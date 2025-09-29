import os
import sqlite3
from pathlib import Path
import json
from datetime import datetime

DB_PATH = os.getenv('DB_PATH', '/tmp/messages.db')

def init_db():
    try:
        Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS contact_messages (
                id TEXT PRIMARY KEY,
                feedback TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS webhook_logs (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid TEXT,
                data TEXT
            )
            """
        )

def save_message(contact_id: str, feedback: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO contact_messages (id, feedback) VALUES (?, ?)",
            (contact_id, feedback),
        )

def get_message(contact_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT feedback FROM contact_messages WHERE id = ?",
            (contact_id,),
        )
        row = cur.fetchone()
        return row[0] if row else None
    
def db_capture_webhook(method: str, uuid: str, url: str, body: str, headers: dict):
    data = {
        "method": method,
        "url": url,
        "body": body,
        "headers": headers,
        "timestamp": int(datetime.now().timestamp())
    }
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO webhook_logs (uuid, data) VALUES (?, ?)",
            (uuid, json.dumps(data)),
        )
        
def db_view_webhook(uuid: str):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT pk, data FROM webhook_logs WHERE uuid = ?",
            (uuid,)
        )
        rows = cur.fetchall()
        result = {pk: json.loads(data) for pk, data in rows}
    return result if rows else None
    