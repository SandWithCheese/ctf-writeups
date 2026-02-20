#!/usr/bin/env python3
import re

# Read the bundle
with open('index.android.bundle', 'rb') as f:
    data = f.read()

# Search for CJ{ pattern
flag_pattern = rb'CJ\{[^\}]{10,50}\}'
matches = re.findall(flag_pattern, data)
if matches:
    print("[+] Found potential flags:")
    for match in matches:
        print(f"  - {match}")

# Search for number arrays that might be encoded
print("\n[+] Searching for suspicious number arrays...")
for i in range(len(data) - 100):
    chunk = data[i:i+100]
    # Look for arrays of numbers that might be ASCII
    if chunk.count(b',') > 10:
        try:
            text = chunk.decode('latin1', errors='ignore')
            if 'CJ' in text or 'flag' in text.lower():
                print(f"[*] Found at offset {hex(i)}: {text[:80]}")
        except:
            pass

print("\n[+] Done")
