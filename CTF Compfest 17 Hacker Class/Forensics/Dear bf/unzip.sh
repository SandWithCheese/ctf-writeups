#!/bin/bash

# Extract all .zip files in the current directory using 7z
for zipfile in *.zip; do
    if [[ -f "$zipfile" ]]; then
        echo "Extracting: $zipfile"
        7z x "$zipfile"
    fi
done
