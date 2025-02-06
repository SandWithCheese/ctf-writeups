#!/usr/bin/env python3
import os
import secrets
from Crypto.Util.strxor import strxor

def initialMagic(u):
    u ^= (u << 31) & 0xFFFFFFFFFFFFFFFF 
    u ^= (u >> 19)
    u ^= (u << 13) & 0xFFFFFFFFFFFFFFFF
    return u & 0xFFFFFFFFFFFFFFFF

def combiningMagic(x):
    x[0] = initialMagic(x[0])
    x[1] = initialMagic(x[1])
    return x[0] ^ x[1]

def splittingMagic(d, s):
    o = b''
    for i in range(0, len(d), 8):
        b = d[i:i+8]
        k = combiningMagic(s)
        c = (int.from_bytes(b, 'little') ^ k).to_bytes(8, 'little')
        print(c)
        o += c[:len(b)]
    
    print(o)
    return o

def run():
    f = os.environ.get('FLAG', 'REDACT').encode()
    k = secrets.token_bytes(len(f))
    p = k.hex().encode() + strxor(k, f)
    x1 = secrets.randbelow(1 << 64)
    x2 = secrets.randbelow(1 << 64)
    s = [x1 & 0xFFFFFFFFFFFFFFFF, x2 & 0xFFFFFFFFFFFFFFFF]
    e = splittingMagic(p, s)
    with open("test.txt", "w") as output_file:
        output_file.write(e.hex())

if __name__ == '__main__':
    run()

