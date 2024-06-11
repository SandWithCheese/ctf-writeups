import os
from Crypto.Cipher import AES
from SecretSharing import Shamir
from flag import FLAG

KEY = os.urandom(16)
res = Shamir.split(5, 5, KEY)
open("out.txt", "w+").write(str(res))
cipher = AES.new(KEY, AES.MODE_ECB)
open("flag.enc", "w+").write(cipher.decrypt(FLAG).hex())