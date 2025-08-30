#!/bin/bash

for file in secret*.zip; do
    # Skip if not a regular file
    [[ -f "$file" ]] || continue

    fixed_name="fixed_$file"

    echo "[*] Fixing: $file → $fixed_name"

    # Copy and replace the first byte (0x17 → 0x50)
    cp "$file" "$fixed_name"
    printf '\x50' | dd of="$fixed_name" bs=1 count=1 seek=0 conv=notrunc status=none

    echo "    [+] Fixed header on $fixed_name"
done

echo "[✓] All done fixing headers."
