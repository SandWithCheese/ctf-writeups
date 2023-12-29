from Crypto.Cipher import AES
from Crypto.Util.Padding import *

plainkey = bytes.fromhex(
    "a72f733ee95c933f1582e4a57beb636c626ce0ff7007c2a766e9d84215f09279"
)[:-16]
iv2 = b"2\x9b7Z\xe7\xa9;\xcaK8@.\x00\xb4\x7f\xf6"
enccode = b"CN\x15\x03\xf8\x14\xdd\x10\x82\xb5#\x8fq\x8c2\xa0\xc8\xfd\x1c\x83rC\x01o\xeev\x0fu\xdfOh\xedk\xe7\x92~+H\tT3y#d\xecj\xae[\xe9g\xdfvq"

flag = b""
for i in range(256):
    for j in range(256):
        key = plainkey + (chr(i).encode() + chr(j).encode()) * 8
        if len(key) == 32:
            cipher = AES.new(key, AES.MODE_CBC, iv2)
            decrypt = cipher.decrypt(pad(enccode, 16))
            if b"Very" in decrypt:
                flag = decrypt
                break
