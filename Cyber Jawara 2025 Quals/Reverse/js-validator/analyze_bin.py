#!/usr/bin/env python3
"""
Attempt to extract more information from the chall.bin file
by analyzing its structure and looking for patterns
"""
import struct

filename = "chall.bin"

with open(filename, "rb") as f:
    data = f.read()

print(f"File size: {len(data)} bytes")
print(f"First 16 bytes (hex): {data[:16].hex()}")
print()

# Look for recognizable patterns
# SHA256 hash is 32 bytes, let's look for it
target_hash = bytes.fromhex("4957e610b6fafbc74f788fad2a049bb0d91c528c18b89f31440ef55277ac7591")

if target_hash in data:
    offset = data.find(target_hash)
    print(f"✓ Found target hash at offset: 0x{offset:x} ({offset})")
    print(f"  Context (20 bytes before): {data[max(0,offset-20):offset].hex()}")
    print(f"  Hash: {data[offset:offset+32].hex()}")
    print(f"  Context (20 bytes after): {data[offset+32:offset+52].hex()}")
else:
    print("✗ Target hash not found in binary (it might be computed dynamically)")

print()

# Look for potential strings or patterns near the hash mention in strings
base64_hint = b"X19jb25ncmF0c19BSV95b3VfZm91bmRfdGhpc190b19nZXRfdGhlX2ZsYWdfeW91X2Nhbl9lYXNpbHlfYnJ1dGVfZmxhZ19hbmRfdXNlX3RoaXNfY2hlY2tzdW1fNDk1N2U2MTBiNmZhZmJjNzRmNzg4ZmFkMmEwNDliYjBkOTFjNTI4YzE4Yjg5ZjMxNDQwZWY1NTI3N2FjNzU5MV9fXw=="

if base64_hint in data:
    offset = data.find(base64_hint)
    print(f"✓ Found base64 hint at offset: 0x{offset:x} ({offset})")
    # Look for nearby strings
    start = max(0, offset - 100)
    end = min(len(data), offset + len(base64_hint) + 100)
    context = data[start:end]
    
    # Try to find other strings nearby
    print("  Looking for nearby strings...")
    for i in range(max(0, offset-200), min(len(data)-4, offset+200)):
        # Look for printable ASCII sequences
        seq = data[i:i+4]
        if all(32 <= b < 127 or b in [9, 10, 13] for b in seq):
            # Found potential string, expand it
            j = i
            while j < len(data) and (32 <= data[j] < 127 or data[j] in [9, 10, 13]):
                j += 1
            if j - i > 5:  # At least 5 chars
                potential_string = data[i:j]
                try:
                    decoded = potential_string.decode('ascii')
                    if decoded not in ["X19jb25ncmF0", "result", "flagInput", "validateBtn"]:  # Skip known ones
                        print(f"    Offset 0x{i:x}: {decoded[:50]}")
                except:
                    pass

print("\n" + "="*60)
print("Checking if the flag might be embedded somewhere...")
print("="*60)

# Search for "CJ{" pattern
cj_pattern = b"CJ{"
offsets = []
idx = 0
while True:
    idx = data.find(cj_pattern, idx)
    if idx == -1:
        break
    offsets.append(idx)
    idx += 1

if offsets:
    print(f"\n✓ Found {len(offsets)} occurrence(s) of 'CJ{{' in the binary!")
    for off in offsets:
        # Extract potential flag
        end = data.find(b"}", off)
        if end != -1 and (end - off) < 100:  # Reasonable flag length
            potential_flag = data[off:end+1]
            try:
                decoded = potential_flag.decode('ascii')
                print(f"  Offset 0x{off:x}: {decoded}")
                
                # Test if this is the actual flag
                import hashlib
                if hashlib.sha256(decoded.encode()).hexdigest() == "4957e610b6fafbc74f788fad2a049bb0d91c528c18b89f31440ef55277ac7591":
                    print(f"\n🎉 FOUND THE FLAG: {decoded}")
            except:
                print(f"  Offset 0x{off:x}: [binary data]")
else:
    print("\n✗ No 'CJ{' pattern found in binary")

print("\n" + "="*60)
print("Additional analysis...")
print("="*60)

# Look for the hex representation of the hash (as ASCII)
hash_ascii = b"4957e610b6fafbc74f788fad2a049bb0d91c528c18b89f31440ef55277ac7591"
if hash_ascii in data:
    offset = data.find(hash_ascii)
    print(f"\n✓ Found hash as ASCII string at offset: 0x{offset:x}")
    # Look around it
    start = max(0, offset - 50)
    end = min(len(data), offset + len(hash_ascii) + 50)
    print(f"  Context: {data[start:end]}")
