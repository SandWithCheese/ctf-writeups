import random
import string
from Crypto.PublicKey import RSA
from libnum import *

def pad(msg: bytes, size: int = 1024//8) -> bytes:
    return msg + (random.choice(string.ascii_uppercase) * (size - len(msg))).encode()

flag = open("flag.txt", "rb").read().strip()

assert(len(flag) == 49)
assert(flag[-1] == b'}'[0])

key = RSA.generate(1164, e=3)
vals = [] 

for i in range(len(flag) // 8):
    pt = flag[::-1][:i]
    pt = s2n(pad(pt))
    vals.append(hex(pow(pt, key.e, key.n)) + "\n")
    
vals.append(hex(pow(s2n(flag), key.e, key.n)) + "\n")
    
with open("out.txt", "w+") as f:
    f.writelines(vals)