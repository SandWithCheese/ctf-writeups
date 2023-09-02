from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os, random, hashlib

with open("flag.txt","rb") as f:
    FLAG = f.read().rstrip()
    f.close()

NBIT = 2048
e = 65537

def get_factor(NBIT: int) -> tuple:
    p, q = getStrongPrime(NBIT//2), getStrongPrime(NBIT//2)
    return (p*q, p, q)

def encrypt(m: int,n: int) -> int:
    return pow(m, e, n)

def encryptFlag(plain: bytes, key: int) -> str:
    IV = os.urandom(16)
    cipher = AES.new(hashlib.sha256(str(key).encode()).digest()[:16], AES.MODE_CBC, iv=IV)
    return (cipher.iv + cipher.encrypt(pad(plain,16))).hex()

def main():
    sizeSlice = len(FLAG) // 4
    
    sliceFLAG = [FLAG[i*sizeSlice:(i+1)*sizeSlice] for i in range(4)]
    list_pub = [random.getrandbits(1024) for _ in range(3)]
    list_priv = [random.getrandbits(256) for _ in range(3)]
    last_priv = random.getrandbits(512)
    S = sum([i*j for i, j in zip(list_pub, list_priv)]) - last_priv

    (n, p, q) = get_factor(NBIT)
    a = random.randint(1,1000)
    b = random.randint(1,1000)
    hint_1 = a * p - b * q
    enc_pub_1 = encrypt(list_pub[0], n)
    list_pub = list_pub[1:] 
    
    LIST_ENC_FLAG = [encryptFlag(plain, key) for plain, key in zip(sliceFLAG, list_priv + [last_priv])]
    
    with open("output.txt","w") as f:
        f.write(f"{LIST_ENC_FLAG = }\n")
        f.write(f"{list_pub = }\n")
        f.write(f"{n = }\n")
        f.write(f"{hint_1 = }\n")
        f.write(f"{enc_pub_1 = }\n")
        f.write(f"{S = }")
        f.close()

if __name__ == "__main__":
    main()