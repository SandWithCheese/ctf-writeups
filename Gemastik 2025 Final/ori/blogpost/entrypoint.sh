#!/usr/bin/env bash
set -e

FLAG_SHA=$(head -c 64 /dev/urandom | sha256sum | awk '{print $1}')
FLAG="GEMASTIK{${FLAG_SHA}}"
echo "$FLAG" > /app/flag.txt
chmod 400 /app/flag.txt

mkdir -p /app/uploads
mkdir -p /data

DBFILE=/data/app.db
if [ ! -f "$DBFILE" ]; then
  echo "Initializing database..."
  sqlite3 $DBFILE < /app/init_db.sql
fi

echo "Starting Flask app (port 8000)..."
export FLASK_APP=/app/app.py
export FLASK_ENV=production

python /app/app.py
