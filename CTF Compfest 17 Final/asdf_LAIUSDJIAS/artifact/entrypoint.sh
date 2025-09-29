#!/bin/sh

set -e

ssh-keygen -A

/usr/sbin/sshd

export ADMIN_KEY=$(head -c 16 /dev/urandom | xxd -p)

echo "COMPFEST17{fake_flag}" > /flag.txt


echo "[*] Starting with ADMIN_KEY=$ADMIN_KEY"

exec su-exec compfest "$@"