generate_secret_key() {
  key=""
  while [ "$(printf "%s" "$key" | wc -c)" -lt 50 ]; do
    key="$(dd if=/dev/urandom bs=32 count=1 2>/dev/null \
      | base64 | tr -dc 'A-Za-z0-9' | cut -c1-50 || true)"
  done
  printf "%s" "$key"
}