#!/usr/bin/env bash
set -euo pipefail

umask 002  # group-writable (helps with bind mounts)

APP_DIR="/app"
UPLOADS_DIR="${APP_DIR}/uploads"
DATA_DIR="/data"
DBFILE="${DATA_DIR}/app.db"
FLAG_FILE="/flag.txt"

mkdir -p "${UPLOADS_DIR}" "${DATA_DIR}"

# Make sure runtime dirs are writable (bind-mounts may ignore chown; that's OK)
chown -R ctfuser:ctfuser "${UPLOADS_DIR}" "${DATA_DIR}" 2>/dev/null || true
chmod 775 "${UPLOADS_DIR}" "${DATA_DIR}" || true

# ------- Start SSH (and set password if provided) -------
if [[ -n "${SSH_PASSWORD:-}" ]]; then
  echo "ctfuser:${SSH_PASSWORD}" | chpasswd || true
fi

if command -v service >/dev/null 2>&1; then
  service ssh start || /usr/sbin/sshd &
else
  /usr/sbin/sshd &
fi
# -------------------------------------------------------

# Initialize DB AS ctfuser (so SQLite can write WAL/SHM next to it)
su -s /bin/bash -c "python - <<'PY'
import app as m
from contextlib import contextmanager

@contextmanager
def ctx():
    with m.app.app_context():
        yield

with ctx():
    # your function should create tables if missing
    m.init_db()
    # OPTIONAL: if you had a generate_flag_at_boot, call it here as well
    try:
        m.generate_flag_at_boot()
    except Exception:
        pass
print('DB initialized by ctfuser.')
PY
" ctfuser

# OPTIONAL: if your filesystem dislikes WAL, uncomment:
# su -s /bin/bash -c \"python - <<'PY'
# import sqlite3
# import os
# db = sqlite3.connect(os.environ.get('DB_PATH', '${DBFILE}'))
# db.execute('PRAGMA journal_mode=DELETE;')
# db.execute('PRAGMA synchronous=NORMAL;')
# db.close()
# print('SQLite journal_mode=DELETE applied.')
# PY
# \" ctfuser

# Secure the flag file if present
if [ -d "${FLAG_FILE}" ]; then
  if [ -f "${FLAG_FILE}" ]; then
    chown root:root "${FLAG_FILE}" || true
    chmod 444 "${FLAG_FILE}" || true
  fi
else
  if [ -f "${FLAG_FILE}" ]; then
    chown root:root "${FLAG_FILE}" || true
    chmod 444 "${FLAG_FILE}" || true
  fi
fi

echo "Starting Flask app on 0.0.0.0:8000 as ctfuser…"
exec su -s /bin/bash -c "cd '${APP_DIR}' && python app.py" ctfuser
