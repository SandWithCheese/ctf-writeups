#!/usr/bin/env python3
"""
Advanced V8 bytecode analyzer
Tries to extract readable code patterns from chall.bin
"""
import re

with open('chall.bin', 'rb') as f:
    data = f.read()

print("=== V8 Bytecode Analysis ===\n")
print(f"File size: {len(data)} bytes\n")

# Try to find JavaScript-like patterns in the bytecode
patterns = [
    (b'function', 'Function definition'),
    (b'=>', 'Arrow function'),
    (b'const ', 'Const declaration'),
    (b'let ', 'Let declaration'),
    (b'var ', 'Var declaration'),
    (b'if(', 'If statement'),
    (b'===', 'Comparison'),
    (b'==', 'Equality check'),
    (b'.value', 'Property access'),
    (b'getElementById', 'DOM access'),
    (b'sha256', 'SHA-256 function'),
    (b'sha512', 'SHA-512 function'),
    (b'hash', 'Hash function'),
]

print("Searching for code patterns...\n")

found_offsets = {}
for pattern, description in patterns:
    offsets = []
    idx = 0
    while True:
        idx = data.find(pattern, idx)
        if idx == -1:
            break
        offsets.append(idx)
        idx += 1
    
    if offsets:
        print(f"✓ Found '{pattern.decode('utf-8', errors='ignore')}' ({description}): {len(offsets)} occurrence(s)")
        found_offsets[pattern] = offsets
        
        # Show context around first occurrence
        if offsets:
            offset = offsets[0]
            start = max(0, offset - 50)
            end = min(len(data), offset + 100)
            context = data[start:end]
            try:
                decoded = context.decode('utf-8', errors='ignore')
                print(f"  Context: {decoded[:150]}")
            except:
                print(f"  Context: {context[:150]}")
        print()

# Look for the validation logic by finding code near "CORRECT FLAG"
correct_flag_offset = data.find(b'CORRECT FLAG')
if correct_flag_offset != -1:
    print(f"\n=== Code near 'CORRECT FLAG' (offset {hex(correct_flag_offset)}) ===\n")
    
    # Extract a large chunk around it
    start = max(0, correct_flag_offset - 500)
    end = min(len(data), correct_flag_offset + 500)
    chunk = data[start:end]
    
    # Try to decode
    try:
        decoded = chunk.decode('utf-8', errors='ignore')
        print(decoded)
    except:
        print("Could not decode as UTF-8")
        # Show hex
        print(chunk.hex())

# Try to find hash comparison
target_hash = b"4957e610b6fafbc74f788fad2a049bb0d91c528c18b89f31440ef55277ac7591"
hash_offset = data.find(target_hash)

if hash_offset == -1:
    print("\n✗ Target hash not found as plaintext in binary")
    print("  It might be computed or encoded differently")
else:
    print(f"\n✓ Found target hash at offset {hex(hash_offset)}")
    start = max(0, hash_offset - 200)
    end = min(len(data), hash_offset + 300)
    chunk = data[start:end]
    try:
        decoded = chunk.decode('utf-8', errors='ignore')
        print(decoded)
    except:
        pass

print("\n=== Summary ===")
print("""
The binary contains:
- Cryptographic references: SHA512, SHA1, AES_ECB, DES_ENCRYPT
- Encoding: BASE64, BASE85, BASE32
- DOM elements: flagInput, validateBtn, result
- The misleading Base64 hint

Next steps:
1. The validation code is in V8 bytecode format
2. Use View8 or Ghidra to properly decompile
3. Or use runtime analysis (memory dump with sudo)
4. Or fix DevTools access in NW.js
""")
