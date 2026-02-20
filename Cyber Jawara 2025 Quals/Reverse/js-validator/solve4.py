#!/usr/bin/env python3
import hashlib
import itertools

target_hash = "4957e610b6fafbc74f788fad2a049bb0d91c528c18b89f31440ef55277ac7591"

def test(s):
    return hashlib.sha256(s.encode()).hexdigest() == target_hash

# Looking at the strings more carefully, let me try specific patterns
# The challenge mentions "easily brute" - so it's probably VERY short

print("Testing very short flags (1-4 chars)...")

# Try single chars
for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-!@#":
    if test(f"CJ{{{c}}}"):
        print(f"FOUND: CJ{{{c}}}")
        exit(0)

# Try 2 chars
charset = "abcdefghijklmnopqrstuvwxyz0123456789_"
for a, b in itertools.product(charset, repeat=2):
    s = a + b
    if test(f"CJ{{{s}}}"):
        print(f"FOUND: CJ{{{s}}}")
        exit(0)

# Try common abbreviations and short words
short_words = [
    "ez", "gg", "wp", "lol", "omg", "wtf", "thx", "brb", "afk",
    "js", "nw", "v8", "bin", "jsc", "vm", "cpu", "ram", "api",
    "sha", "md5", "aes", "rsa", "des", "ecb", "cbc",
    "b64", "b32", "b85", "hex", "bin",
    "cj", "ctf", "pwn", "rev", "web", "cry", "for", "mis"
]

print("Testing short words and abbreviations...")
for word in short_words:
    variations = [
        word,
        word.upper(),
        word.capitalize(), 
        f"{word}!",
        f"_{word}_",
        f"{word}1",
        f"1{word}",
    ]
    for v in variations:
        if test(f"CJ{{{v}}}"):
            print(f"FOUND: CJ{{{v}}}")
            exit(0)

# Try numbers
print("Testing number patterns...")
for i in range(10000):
    if test(f"CJ{{{i}}}"):
        print(f"FOUND: CJ{{{i}}}")
        exit(0)

# Try combinations of 2 short words
print("Testing 2-word combinations...")
for w1, w2 in itertools.combinations(short_words[:20], 2):
    for sep in ["", "_", "-"]:
        s = f"{w1}{sep}{w2}"
        if test(f"CJ{{{s}}}"):
            print(f"FOUND: CJ{{{s}}}")
            exit(0)

print("No match found. The flag might be longer than expected.")
