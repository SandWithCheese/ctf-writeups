#!/usr/bin/env python3
"""
Search for app-specific logic in the decompiled hermes output
"""

with open('decompiled_output.js', 'r', errors='ignore') as f:
    lines = f.readlines()

# Search for lines with interesting constants/patterns
print("[+] Searching for suspicious array assignments...")
for i, line in enumerate(lines):
    # Look for array assignments with numbers
    if 'new Array(' in line and i < len(lines) - 20:
        # Print context
        context = ''.join(lines[max(0, i-5):min(len(lines), i+20)])
        if len(context) < 2000 and ('67' in context or '74' in context or '123' in context):
            print(f"\n[*] Found at line {i}:")
            print(context[:1000])
            print("---")

print("\n[+] Done")
