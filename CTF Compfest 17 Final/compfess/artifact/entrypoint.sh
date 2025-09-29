#!/bin/sh
set -eu

log() {
  printf "[%s] [web:%s] %s\n" "$(date -Iseconds)" "$$" "$*" 1>&2
}

chmod -R 755 /app
chmod 757 /app/src/main/tests.py

generate_secret_key() {
  key=""
  while [ "$(printf "%s" "$key" | wc -c)" -lt 50 ]; do
    key="$(dd if=/dev/urandom bs=32 count=1 2>/dev/null \
      | base64 | tr -dc 'A-Za-z0-9' | cut -c1-50 || true)"
  done
  printf "%s" "$key"
}

cleanup() {
  if [ -n "${DBMON_PID:-}" ] 2>/dev/null; then
    if kill -0 "$DBMON_PID" 2>/dev/null; then
      log "Stopping DB monitor (pid=${DBMON_PID})"
      kill -TERM "$DBMON_PID" 2>/dev/null || true
      i=0
      while [ $i -lt 10 ]; do
        kill -0 "$DBMON_PID" 2>/dev/null || break
        sleep 0.2
        i=$((i+1))
      done
      kill -KILL "$DBMON_PID" 2>/dev/null || true
    fi
  fi
}
trap cleanup EXIT INT TERM

if ! python /app/src/manage.py makemigrations; then
  if [ -f "${MGMT_INIT}" ] && [ -s "${MGMT_INIT}" ]; then
    log "Clearing ${MGMT_INIT}"
    : > "${MGMT_INIT}"
  fi
fi

python /app/src/manage.py migrate
python /app/src/manage.py generate_admin

# Secret key
: "${DJANGO_SECRET_KEY:=$(generate_secret_key)}"
export DJANGO_SECRET_KEY

crond -f -d 8 &
echo "[entrypoint] cronie started (schedule: every 30 minutes)"

# ----- Start app -----
cd /app/src
log "Starting gunicorn…"

exec su -s /bin/sh -c "exec gunicorn -w 6 -t 0 -b 0.0.0.0:8000 compfess.wsgi:application" django
