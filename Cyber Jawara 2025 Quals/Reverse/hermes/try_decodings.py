#!/usr/bin/env python3
import codecs
import base64

# Potential flag content found
potential = "Cp{{bzLspxy"

# Try ROT13
try:
    rot13 = codecs.encode(potential, 'rot_13')
    print(f"ROT13: CJ{{{rot13}}}")
except Exception as e:
    print(f"ROT13 Error: {e}")

# Try base64 decode (in case it's base64)
try:
    # Add padding if needed
    padded = potential + '=' * ((4 - len(potential) % 4) % 4)
    b64 = base64.b64decode(padded)
    print(f"Base64: CJ{{{b64}}}")
except Exception as e:
    print(f"Not base64: {e}")

# Check if it's ASCII shift
shifted_plus = ''.join([chr((ord(c) + 1) % 256) if c.isalpha() else c for c in potential])
print(f"Shifted +1: CJ{{{shifted_plus}}}")

shifted_minus = ''.join([chr((ord(c) - 1) % 256) if c.isalpha() else c for c in potential])
print(f"Shifted -1: CJ{{{shifted_minus}}}")

# Print as-is
print(f"\nOriginal: CJ{{{potential}}}")
