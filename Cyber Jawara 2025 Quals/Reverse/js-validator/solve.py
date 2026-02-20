#!/usr/bin/env python3
import hashlib
import string
import itertools

# The checksum we found in the binary
target_hash = "4957e610b6fafbc74f788fad2a049bb0d91c528c18b89f31440ef55277ac7591"

# Flag format: CJ{...}
# We need to brute force the content inside the braces

# Let's try different approaches
def sha256(s):
    return hashlib.sha256(s.encode()).hexdigest()

def sha512(s):
    return hashlib.sha512(s.encode()).hexdigest()

# First, let's check if it's just a simple flag
print(f"Target hash: {target_hash}")
print(f"Hash length: {len(target_hash)} chars")

# The hash is 64 chars, which matches SHA-256 or SHA-512 (first 64 chars)
print("\nTrying SHA-256...")

# Let's try some common patterns
common_words = [
    "flag", "test", "password", "admin", "cyber", "jawara", "2025", 
    "quals", "reverse", "javascript", "nwjs", "validator",
    "congrats", "you_found_it", "easy", "brute", "checksum"
]

# Try simple flags
for word in common_words:
    flag = f"CJ{{{word}}}"
    if sha256(flag) == target_hash:
        print(f"Found flag: {flag}")
        exit()

# Try combinations of words
for w1, w2 in itertools.combinations(common_words, 2):
    for sep in ["", "_", "-"]:
        flag = f"CJ{{{w1}{sep}{w2}}}"
        if sha256(flag) == target_hash:
            print(f"Found flag: {flag}")
            exit()

# Let's try brute forcing with printable characters
# Start with shorter lengths and work up
charset = string.ascii_letters + string.digits + "_-!@#$%^&*()"

print("\nBrute forcing... This might take a while")
print("Trying lengths from 1 to 20...")

for length in range(1, 21):
    print(f"Trying length {length}...")
    if length <= 6:  # Only brute force short lengths
        for attempt in itertools.product(charset, repeat=length):
            content = ''.join(attempt)
            flag = f"CJ{{{content}}}"
            if sha256(flag) == target_hash:
                print(f"\nFound flag: {flag}")
                exit()

print("\nNo flag found with simple brute force. Let's try analyzing the binary more.")
