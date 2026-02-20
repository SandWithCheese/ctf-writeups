#!/usr/bin/env python3
import hashlib

hashes = [
    "274e21507fce26a09c731cb2a89f6702",
    "46a6b2e302e71d822b6d3c9cf50abe60",
    "7da2397d138b0354f2d6024b0ae29a65",
    "96b8dcedcbde55e4d4363ff1137fb56e",
    "c09797ed8039245eacbc8afc05d71795",
    "db5314760fd7298555bab342c1137312",
    "e1bcc7900f46a863a697dda45d68834c",
    "e3caba93d519b11dcb06c807c4924287",
    "f8f8bbe836118c7be1d6e8edab1c2b30",
]

# Try single characters (likely keystrokes)
print("Testing single characters...")
for char_code in range(256):
    char = chr(char_code)
    h = hashlib.md5(char.encode()).hexdigest()
    if h in hashes:
        print(f"  {h} = '{char}' (ASCII {char_code})")

# Try common keys
print("\nTesting special keys...")
special_keys = [
    "Enter",
    "Return",
    "Space",
    "Tab",
    "Backspace",
    "Shift",
    "Ctrl",
    "Alt",
    "CapsLock",
    "Escape",
    "F1",
    "F2",
    "F3",
    "F4",
    "F5",
    "F6",
    "F7",
    "F8",
    "F9",
    "F10",
    "F11",
    "F12",
    "Up",
    "Down",
    "Left",
    "Right",
    "Home",
    "End",
    "PageUp",
    "PageDown",
    "Delete",
    "Insert",
]

for key in special_keys:
    h = hashlib.md5(key.encode()).hexdigest()
    if h in hashes:
        print(f"  {h} = '{key}'")

# Try lowercase keys with "Key_" prefix (common in keyloggers)
print("\nTesting Key_ prefixed values...")
for char in "abcdefghijklmnopqrstuvwxyz0123456789":
    for prefix in ["Key_", "key_", "", "KEY_"]:
        test = f"{prefix}{char}"
        h = hashlib.md5(test.encode()).hexdigest()
        if h in hashes:
            print(f"  {h} = '{test}'")

# Try numbers and special characters
print("\nTesting numbers and special characters...")
for char in "0123456789!@#$%^&*()_+-=[]{}|;':\",./<>?`~":
    h = hashlib.md5(char.encode()).hexdigest()
    if h in hashes:
        print(f"  {h} = '{char}' (ASCII {ord(char)})")
