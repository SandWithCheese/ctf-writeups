#!/usr/bin/env python3
import sys

data = open('index.android.bundle', 'rb').read()
offset = 0x28fee6
xor_key = 122

decoded = []
for i in range(300):
    if offset + i < len(data):
        decoded.append(data[offset + i] ^ xor_key)

decoded_str = ''.join([chr(b) if 32 <= b < 127 else '.' for b in decoded])
print(f"Decoded string: {decoded_str}")

final_flag = "".join([chr(b) if 32 <= b < 127 else "_" for b in decoded[:16]])
print(f"Decoded Candidate: {final_flag}")
print(f"Hex values: {decoded[:16]}")
print(f"Raw bytes at offset: {[hex(b) for b in data[offset:offset+16]]}")

# Show raw bytes around CJ{
print(f"\nFirst 50 bytes (hex): {' '.join([f'{b:02x}' for b in decoded[:50]])}")
print(f"First 50 bytes (char): {decoded_str[:50]}")

# Try to extract flag
flag_bytes = bytes(decoded)
try:
    flag_str = flag_bytes.decode('ascii', errors='ignore')
    if '}' in flag_str:
        end_idx = flag_str.index('}') + 1
        print(f"\nFLAG: {flag_str[:end_idx]}")
    else:
        print(f"\nPartial: {flag_str}")
except:
    print(f"\nPartial (with errors): {decoded_str}")
