#!/usr/bin/env python3
import hashlib

# The checksum we found in the binary
target_hash = "4957e610b6fafbc74f788fad2a049bb0d91c528c18b89f31440ef55277ac7591"

def test_hash(flag):
    """Test SHA-256"""
    sha256 = hashlib.sha256(flag.encode()).hexdigest()
    return sha256 == target_hash

# Common CTF flag patterns
patterns = [
    # Based on "easily brute" - maybe it's really simple
    "test", "password", "flag", "admin", "root",
    # Numbers
    "1234", "12345", "123456", "000000", "111111",
    # The challenge name
    "js_validator", "jsvalidator", "js-validator",
    # Event name
    "cj2025", "cj_2025", "cyber_jawara", "cyberjawara",
    # Common CTF
    "easy_flag", "simple_flag", "brute_me", "brute_force",
    # Based on file name
    "chall", "challenge",
    # Really easy ones
    "a", "aa", "aaa", "1", "11", "111",
    # L33t speak
    "fl4g", "3z", "br00t", "ez_br00t", "3z_br00t",
    # Based on the decimal values wesaw in strings
    "4957e610", "7591", "49bb", 
]

print(f"Target hash: {target_hash}\n")
print("Testing common patterns...")

for pattern in patterns:
    variations = [
        pattern,
        pattern.upper(),
        pattern.capitalize(),
        f"_{pattern}_",
        f"{pattern}!",
        f"!{pattern}",
    ]
    
    for var in variations:
        flag = f"CJ{{{var}}}"
        if test_hash(flag):
            print(f"\n✓ FOUND! Flag: {flag}")
            print(f"SHA-256: {hashlib.sha256(flag.encode()).hexdigest()}")
            exit(0)

# Try reading from rockyou if it exists
try:
    print("\nTrying rockyou wordlist...")
    with open('/usr/share/wordlists/rockyou.txt', 'r', encoding='latin-1') as f:
        for i, line in enumerate(f):
            word = line.strip()
            for flag_format in [f"CJ{{{word}}}", f"CJ{{_{word}_}}", f"CJ{{{word.upper()}}}"]:
                if test_hash(flag_format):
                    print(f"\n✓ FOUND! Flag: {flag_format}")
                    exit(0)
            
            if i % 100000 == 0:
                print(f"  Tried {i} words...", end='\r')
            
            if i > 1000000:  # Limit to first 1M words
                break
except FileNotFoundError:
    print("Rockyou wordlist not found, skipping...")

print("\nNo match found with common patterns.")
