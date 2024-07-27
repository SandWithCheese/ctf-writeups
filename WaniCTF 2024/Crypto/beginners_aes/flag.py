# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from os import urandom
import hashlib
from string import printable

key = b"the_enc_key_is_"
iv = b"my_great_iv_is_"
enc = b'\x16\x97,\xa7\xfb_\xf3\x15.\x87jKRaF&"\xb6\xc4x\xf4.K\xd77j\xe5MLI_y\xd96\xf1$\xc5\xa3\x03\x990Q^\xc0\x17M2\x18'
flag_hash = "6a96111d69e015a07e96dcd141d31e7fc81c4420dbbef75aef5201809093210e"


for ci in printable:
    for cj in printable:
        new_key = key + ci.encode()
        new_iv = iv + cj.encode()

        cipher = AES.new(new_key, AES.MODE_CBC, new_iv)

        dec = cipher.decrypt(enc)

        try:
            dec = unpad(dec, 16)
            flag_hash_dec = hashlib.sha256(dec).hexdigest()
            if flag_hash_dec == flag_hash:
                # print(f"key = {new_key}")
                # print(f"iv = {new_iv}")
                # print(f"dec = {dec}")
                # print(f"flag_hash_dec = {flag_hash_dec}")
                print(dec.decode())
                break
        except:
            pass
