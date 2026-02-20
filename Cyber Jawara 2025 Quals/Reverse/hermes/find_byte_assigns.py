#!/usr/bin/env python3
import re

print("Searching for byte sequence assignments...")
target_values = [57, 48, 1, 57, 10, 1]

with open('decompiled_output.js', 'r') as f:
    lines = f.readlines()

for i in range(len(lines) - 20):
    # Check a window of lines
    window = lines[i:i+20]
    window_text = ''.join(window)
    
    # Check if all target values appear in assignments like " = 57;"
    matches = 0
    for val in target_values:
        if f"= {val};" in window_text:
            matches += 1
            
    if matches >= 4:
        print(f"\n[!] Found potential match at line {i}:")
        print(window_text)
