#!/bin/bash

# Loop through all files in the current directory
for file in *; do
    if [[ -f "$file" ]]; then
        echo "[+] Searching in: $file"
        strings "$file" | grep --color=always "COMPFEST17"
    fi
done
