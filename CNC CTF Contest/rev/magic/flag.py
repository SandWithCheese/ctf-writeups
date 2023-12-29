from Crypto.Cipher import ARC4
from Crypto.Hash import SHA256, HMAC
from libnum import n2s

# from secrets import flag
import random

random.seed(42069)
flag = bytes.fromhex(
    "c7de3a02e130a5a70e6d0169437460b2769a31f9226d799e1a6d244d01bbf39972621e19"
)
key = n2s(random.getrandbits(512))
nonce = n2s(random.getrandbits(512))
tempkey = HMAC.new(key, nonce, SHA256).digest()
cipher = ARC4.new(tempkey)
print(cipher.decrypt(flag).decode())
