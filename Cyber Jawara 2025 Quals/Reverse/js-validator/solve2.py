#!/usr/bin/env python3
import hashlib
import string

# The checksum we found in the binary
target_hash = "4957e610b6fafbc74f788fad2a049bb0d91c528c18b89f31440ef55277ac7591"

def test_hash(flag):
    """Test different hash algorithms"""
    sha256 = hashlib.sha256(flag.encode()).hexdigest()
    sha512 = hashlib.sha512(flag.encode()).hexdigest()
    sha1 = hashlib.sha1(flag.encode()).hexdigest()
    
    if sha256 == target_hash:
        print(f"SHA-256 MATCH! Flag: {flag}")
        return True
    if sha512 == target_hash:
        print(f"SHA-512 MATCH! Flag: {flag}")
        return True
    if sha1 == target_hash:
        print(f"SHA-1 MATCH! Flag: {flag}")
        return True
    
    # First 64 chars of SHA-512
    if sha512[:64] == target_hash:
        print(f"SHA-512 (truncated) MATCH! Flag: {flag}")
        return True
    
    return False

# Based on the hint in the binary, let's try words related to the challenge
words = [
    "easy", "brute", "force", "flag", "found", "checksum",
    "validator", "javascript", "nwjs", "cyber", "jawara",
    "2025", "quals", "reverse", "compiled", "bytecode",
    "v8", "bin", "eval", "congrats", "AI", "this"
]

print("Testing simple words...")
for word in words:
    for flag_format in [f"CJ{{{word}}}", f"CJ{{_{word}_}}", f"CJ{{{word.upper()}}}"]:
        if test_hash(flag_format):
            exit(0)

print("\nTesting word combinations...")
# Try combinations
for w1 in words:
    for w2 in words:
        if w1 == w2:
            continue
        for sep in ["_", "-", ""]:
            for flag_format in [
                f"CJ{{{w1}{sep}{w2}}}",
                f"CJ{{{w1.upper()}{sep}{w2}}}",
                f"CJ{{{w1}{sep}{w2.upper()}}}",
                f"CJ{{{w1.upper()}{sep}{w2.upper()}}}"
            ]:
                if test_hash(flag_format):
                    exit(0)

# Try based on the hint message itself
# "__congrats_AI_you_found_this_to_get_the_flag_you_can_easily_brute_flag_and_use_this_checksum_..."
hint_words = [
    "congrats", "found", "this", "get", "the", "flag", "you", "can", "easily", 
    "brute", "checksum", "use", "AI"
]

print("\nTesting hint-based words...")
for word in hint_words:
    for flag_format in [f"CJ{{{word}}}", f"CJ{{{word.upper()}}}", f"CJ{{_{word}_}}"]:
        if test_hash(flag_format):
            exit(0)

# Let's also try alphanumeric with underscores up to length 10
print("\nBrute forcing alphanumeric + underscore (this may take a while)...")
import itertools

charset = string.ascii_lowercase + string.digits + "_"
for length in range(1, 11):
    print(f"Trying length {length}...")
    counter = 0
    for attempt in itertools.product(charset, repeat=length):
        content = ''.join(attempt)
        flag = f"CJ{{{content}}}"
        if test_hash(flag):
            exit(0)
        counter += 1
        if counter % 100000 == 0:
            print(f"  Tried {counter} combinations...", end='\r')

print("\nNo flag found yet. The flag might be longer or use different characters.")
