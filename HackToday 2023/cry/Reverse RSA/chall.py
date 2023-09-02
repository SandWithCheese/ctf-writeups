from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random
import os
import hashlib

def generate_prime():
    while True:
        a,b = random.getrandbits(512), random.getrandbits(512)
        if isPrime(pow(a+b,2) - 2*a*b):
            return pow(a+b,2) - 2*a*b,a,b

def encrypt(m: str, a: int, b: int):
    key1 = hashlib.sha256(long_to_bytes(a)).digest()[:16]
    key2 = hashlib.sha256(long_to_bytes(b)).digest()[:16]
    enc = AES.new((key1+key2), AES.MODE_ECB)
    return enc.encrypt(pad(m.encode(),16)).hex()

def hehe():
    e = 3
    m = open("flag.txt", "r").read()
    while True:
        p,a1,b1 = generate_prime()
        q,a2,b2 = generate_prime()
        phi = (p-1)*(q-1)
        d = inverse(e,phi)
        if d > 1:
            break
    return [encrypt(m[:len(m)//2],a1,b1), encrypt(m[len(m)//2:],a2,b2)],p,q,e,phi,d

def main():
    c = os.urandom(128)
    c = bytes_to_long(c)
    arr,p,q,e,phi,d = hehe()
    n = p*q
    c = pow(c,e,n)
    with open("output.txt", "w") as f:
        f.write(f"{arr = }\n")
        f.write(f"{n = }\n")
        f.write(f"hint1 = {pow(d,e,n)}\n")
        f.write(f"hint2 = {pow(phi,e,n)}\n")
        f.write(f"{c = }\n")
    
if __name__ == "__main__":
    main()