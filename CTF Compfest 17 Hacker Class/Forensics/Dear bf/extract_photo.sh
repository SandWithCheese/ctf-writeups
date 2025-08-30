#!/bin/bash

echo "[*] Searching image files for any hidden flag-looking strings..."

rm -f photo_strings.txt

for i in {64..80}; do
    if [[ -f photo$i.png ]]; then
        strings photo$i.png >> photo_strings.txt
    elif [[ -f photo$i.jpg ]]; then
        strings photo$i.jpg >> photo_strings.txt
    fi
done

echo "[*] Results with flag patterns:"
grep -E 'COMPFEST|{|\}' photo_strings.txt
