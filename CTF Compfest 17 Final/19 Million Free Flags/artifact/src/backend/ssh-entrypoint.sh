#!/bin/sh
set -e

ssh-keygen -A

/usr/sbin/sshd -D &
SSHD_PID=

cleanup() {
  if kill -0 "" 2>/dev/null; then
    kill ""
    wait ""
  fi
}

trap cleanup EXIT INT TERM

cd /srv/app

exec su -s /bin/sh app -c "node src/index.js"
