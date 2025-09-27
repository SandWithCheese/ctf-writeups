find binwalk_out -type f -name 'decompressed.bin' -size -200k -print |
  head -n 120 | while read -r f; do
    if jq -e type >/dev/null 2>&1 <"$f"; then
      echo "=== JSON: $f ==="
      # Show top-level keys
      jq 'keys_unsorted' <"$f" 2>/dev/null || true
      # Try common fields that might hold path/name/content
      jq -r '.name?, .path?, .filename?, .file?, .target?, .dst?, .src?, .content?, .data?' <"$f" 2>/dev/null | sed -n '1,60p'
      echo
    fi
  done