#!/usr/bin/env python3
import hashlib
from collections import Counter

# Read the hashes
with open("/tmp/hashes.txt", "r") as f:
    hashes = [line.strip() for line in f]

print(f"Total hashes: {len(hashes)}")
print(f"Unique hashes: {len(set(hashes))}")
print("\nFrequency distribution:")
counter = Counter(hashes)
for hash_val, count in counter.most_common():
    print(f"  {hash_val}: {count} times")

print("\n" + "=" * 80)
print("Trying Virtual Key codes (VK_*)...")
vk_codes = {
    0x08: "VK_BACK",
    0x09: "VK_TAB",
    0x0D: "VK_RETURN",
    0x10: "VK_SHIFT",
    0x11: "VK_CONTROL",
    0x12: "VK_MENU",
    0x14: "VK_CAPITAL",
    0x1B: "VK_ESCAPE",
    0x20: "VK_SPACE",
    0x21: "VK_PRIOR",
    0x22: "VK_NEXT",
    0x23: "VK_END",
    0x24: "VK_HOME",
    0x25: "VK_LEFT",
    0x26: "VK_UP",
    0x27: "VK_RIGHT",
    0x28: "VK_DOWN",
    0x2D: "VK_INSERT",
    0x2E: "VK_DELETE",
}

# Add 0-9, A-Z
for i in range(ord("0"), ord("9") + 1):
    vk_codes[i] = chr(i)
for i in range(ord("A"), ord("Z") + 1):
    vk_codes[i] = chr(i)

unique_hashes = set(hashes)
cracked = {}

# Try VK codes as hex strings
for vk, name in vk_codes.items():
    test_str = f"{vk:02X}"
    h = hashlib.md5(test_str.encode()).hexdigest()
    if h in unique_hashes:
        cracked[h] = f"VK:{name} ({test_str})"
        print(f"  {h} = {name} (VK code: 0x{test_str})")

# Try as decimal strings
for vk, name in vk_codes.items():
    test_str = str(vk)
    h = hashlib.md5(test_str.encode()).hexdigest()
    if h in unique_hashes:
        cracked[h] = f"VK:{name} (decimal {test_str})"
        print(f"  {h} = {name} (VK code: {vk})")

# Try the character itself
print("\n" + "=" * 80)
print("Trying direct ASCII characters...")
for i in range(32, 127):
    char = chr(i)
    h = hashlib.md5(char.encode()).hexdigest()
    if h in unique_hashes:
        cracked[h] = char
        print(f"  {h} = '{char}' (ASCII {i})")

# Try uppercase/lowercase variations
print("\n" + "=" * 80)
print("Trying case variations...")
for char in "abcdefghijklmnopqrstuvwxyz":
    for test in [char, char.upper()]:
        h = hashlib.md5(test.encode()).hexdigest()
        if h in unique_hashes:
            cracked[h] = test
            print(f"  {h} = '{test}'")

print("\n" + "=" * 80)
if cracked:
    print(f"\nCracked {len(cracked)} / {len(unique_hashes)} unique hashes")
    print("\nReconstructing sequence:")
    result = []
    for h in hashes:
        if h in cracked:
            result.append(cracked[h])
        else:
            result.append(f"[{h}]")
    print("".join(result))
else:
    print("\nNo matches found yet. Need to try more patterns.")
