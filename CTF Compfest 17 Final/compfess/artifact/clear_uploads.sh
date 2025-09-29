#!/bin/sh
set -eu

REPORTS_DIR="/upload/reports"

log() {
  printf "[%s] [clear_reports] %s\n" "$(date -Iseconds)" "$*" 1>&2
}

if [ -d "$REPORTS_DIR" ]; then
  rm -rf "$REPORTS_DIR"/*
  log "Cleared contents of $REPORTS_DIR"
else
  log "Directory $REPORTS_DIR does not exist"
fi
