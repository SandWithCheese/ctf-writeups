#!/usr/bin/env python3
"""
Find interesting data patterns in the Hermes bundle that might be the flag
"""
import struct

with open('index.android.bundle', 'rb') as f:
    data = f.read()

print("[+] Searching for encoded flag patterns...")

# Look for sequences of bytes that might be XOR'd with a simple key
# CJ{ = 67, 74, 123
target_start = [67, 74, 123]

# Search for XOR patterns
for xor_key in range(1, 256):
    encoded = [(target_start[0] ^ xor_key), (target_start[1] ^ xor_key), (target_start[2] ^ xor_key)]
    pattern = bytes(encoded)
    
    idx = data.find(pattern)
    if idx != -1:
        # Found potential XOR encoded flag
        print(f"\n[*] Potential XOR key: {xor_key} (0x{xor_key:02x})")
        print(f"    Found at offset: 0x{idx:x}")
        
        # Try to decode next 50 bytes
        decoded = []
        for i in range(50):
            if idx + i < len(data):
                decoded.append(data[idx + i] ^ xor_key)
        
        decoded_str = ''.join([chr(b) if 32 <= b < 127 else '.' for b in decoded])
        print(f"    Decoded (50 bytes): {decoded_str}")
        
        # Check if it looks like a valid flag
        try:
            full_decoded = bytes(decoded).decode('ascii', errors='ignore')
            if 'CJ{' in full_decoded and '}' in full_decoded:
                end_idx = full_decoded.index('}') + 1
                print(f"\n[!] POTENTIAL FLAG FOUND: {full_decoded[:end_idx]}")
        except:
            pass

# Also look for base64 encoded flags
print("\n[+] Searching for base64 patterns...")
import re
import base64

# CJ{ in base64 could be Q0p7 (if "CJ{" is the start)
base64_patterns = [b'Q0p7', b'Q0o', b'Qzp', b'Qko']

for pattern in base64_patterns:
    idx = data.find(pattern)
    if idx != -1:
        print(f"\n[*] Found base64 pattern {pattern} at 0x{idx:x}")
        # Extract surrounding context
        start = max(0, idx - 10)
        end = min(len(data), idx + 100)
        context = data[start:end]
        
        # Try to find valid base64 string
        text = context.decode('latin1', errors='ignore')
        # Look for base64-like strings
        base64_candidates = re.findall(r'[A-Za-z0-9+/=]{20,}', text)
        for candidate in base64_candidates[:3]:
            try:
                decoded = base64.b64decode(candidate)
                decoded_str = decoded.decode('ascii', errors='ignore')
                if 'CJ' in decoded_str or 'flag' in decoded_str.lower():
                    print(f"    Decoded: {decoded_str}")
            except:
                pass

print("\n[+] Done")
