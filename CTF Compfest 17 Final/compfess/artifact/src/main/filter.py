
from .models import Menfess
from typing import List
from django.db import connection

blacklist = ['admin','flag','/','cat','*','copy','program','drop','update','delete','create','select','os','=','||','concat','+','echo','overlay','decode','encode','replace','reverse','\\']

def validate(username):
    if not username.isascii():
        raise ValueError("Username can only be ascii characters")
    for char in blacklist:
        if char in username.lower():
            raise ValueError("Your username contains prohibited characters")
    return username

def _rows_to_menfess_list(rows) -> List[Menfess]:
    """
    Convert list of (id, ...) rows to ordered Menfess objects using a single ORM fetch.
    Keeps template compatibility (needs .recipient, .sender_user).
    """
    ids = [row[0] for row in rows]
    if not ids:
        return []
    menfess_map = Menfess.objects.select_related('recipient', 'sender_user').in_bulk(ids)
    return [menfess_map[i] for i in ids if i in menfess_map]

def filter_by_sender(username):
    username = validate(username)
    with connection.cursor() as cur:
        cur.execute(f"""
        SELECT m.id, m.content, m.created_at, m.sender_user_id, m.is_guest, m.recipient_id
        FROM main_menfess AS m JOIN auth_user AS u ON m.sender_user_id = u.id WHERE u.username = '{username}' ORDER BY m.created_at DESC LIMIT 200""")
        rows = cur.fetchall()
    return _rows_to_menfess_list(rows)

def filter_by_guest():
    with connection.cursor() as cur:
        cur.execute("""
        SELECT id, content, created_at, sender_user_id, is_guest, recipient_id
        FROM main_menfess
        WHERE is_guest = TRUE
        ORDER BY created_at DESC
        LIMIT 200
    """)
        rows = cur.fetchall()
    return _rows_to_menfess_list(rows)
