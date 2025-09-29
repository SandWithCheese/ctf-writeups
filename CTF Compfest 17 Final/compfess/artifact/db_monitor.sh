#!/bin/sh
set -eu

DB_NAME="${DB_NAME:-compfess}"
DB_SIZE_LIMIT_MB="${DB_SIZE_LIMIT_MB:-800}"
ADMIN_USERNAME="${ADMIN_USERNAME:-haiakuadmintcompfess}"

: "${PGHOST:=db}"
: "${PGPORT:=5432}"
: "${PGUSER:=compfess}"
: "${PGPASSWORD:=compfess}"
export PGHOST PGPORT PGUSER PGPASSWORD

log() {
  printf "[%s] [db_monitor] %s\n" "$(date -Iseconds)" "$*" 1>&2
}

# check size
db_bytes="$(psql -d "$DB_NAME" -tAc "SELECT pg_database_size(current_database());" 2>/dev/null || echo 0)"
db_pretty="$(psql -d "$DB_NAME" -tAc "SELECT pg_size_pretty(pg_database_size(current_database()));" 2>/dev/null || echo 0)"
size_mb=$(( (db_bytes + 1024*1024 - 1) / (1024*1024) ))

user_count="$(psql -d "$DB_NAME" -tAc "SELECT COUNT(*) FROM auth_user;" 2>/dev/null || echo 0)"
profile_count="$(psql -d "$DB_NAME" -tAc "SELECT COUNT(*) FROM main_profile;" 2>/dev/null || echo 0)"

log "DB=${db_pretty} (${db_bytes} bytes) | auth_user rows=${user_count} | main_profile rows=${profile_count}"

if [ "$size_mb" -gt "$DB_SIZE_LIMIT_MB" ]; then
  log "DB size ${size_mb}MB exceeded limit ${DB_SIZE_LIMIT_MB}MB. Initiating flush…"

  python /app/src/manage.py shell <<EOF
from django.contrib.auth import get_user_model
from django.core import serializers
from main.models import Profile

User = get_user_model()
u = User.objects.get(username='${ADMIN_USERNAME}')
p, _ = Profile.objects.get_or_create(user=u, defaults={"role":"admin"})
objs = [u, p]
with open('/tmp/admin.json', 'w') as fp:
    fp.write(serializers.serialize('json', objs, use_natural_foreign_keys=True, use_natural_primary_keys=True))
EOF

  python /app/src/manage.py flush --noinput || log "flush failed"
  python /app/src/manage.py loaddata /tmp/admin.json || log "restore failed"
  python /app/src/manage.py generate_admin || log "generate_admin failed"
  rm -f /tmp/admin.json
  log "Flush complete (only admin + profile preserved)."
fi
