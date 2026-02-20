#!/usr/bin/env python3
data_hex = "39 30 01 39 0a 01 01 18 00 36 09 0a 02 6d 03 07 78 00 3f 07 00 fd 73 06 31 00 55 06 09 0a 08 06 07 39 07 01 01 18 00 36 06 07 02 6d 03 01 3f 01"
data = bytes.fromhex(data_hex)

print("Trying dynamic keys on:")
print(data.hex())

def try_key(name, key_func):
    decoded = []
    for i in range(len(data)):
        k = key_func(i) & 0xFF
        decoded.append(data[i] ^ k)
    
    try:
        s = "".join([chr(c) if 32 <= c < 127 else "?" for c in decoded])
        print(f"{name}: {s}")
    except:
        pass

# 1. Decreasing key (z, y, x...) from 122
try_key("Dec from 122", lambda i: 122 - i)

# 2. Increasing key from 122
try_key("Inc from 122", lambda i: 122 + i)

# 3. Key based on index
try_key("Key = index", lambda i: i)

# 4. Key = 122 always (reference)
try_key("Key = 122", lambda i: 122)

# 5. Alternating 122, something else
# If 'Cp' -> 'Cy' (Cyber?), 'p' (112) -> 'y' (121) needs key: 112 ^ 121 = 9.
# 122 is 01111010. 9 is 00001001.

# 6. Try to brute force key to make "CJ{Cy"
# C J { C y ...
# 39 30 01 39 0a ...
# ^ ^ ^ ^ ^
# K1 K2 K3 K4 K5
# C(43) J(4a) {(7b) C(43) y(79)
target = b"CJ{CyberJawara"
print("\nDerived keys for 'CJ{CyberJawara':")
keys = []
for i in range(min(len(target), len(data))):
    k = data[i] ^ target[i]
    keys.append(k)
    print(f"Index {i}: Data {data[i]:02x} ^ Target {target[i]:02x} ({chr(target[i])}) = Key {k:02x}")

print("\nKey sequence:", [hex(k) for k in keys])
