from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from libnum import *

flag = open("flag.txt", "rb").read().strip()

key = RSA.generate(1024)
cipher = PKCS1_OAEP.new(key)
    
with open("../bin/out.txt", "w+") as f:
    f.write(str(key.q) + "\n")
    f.write(str(key.u) + "\n")
    f.write(str(s2n(cipher.encrypt(flag))))