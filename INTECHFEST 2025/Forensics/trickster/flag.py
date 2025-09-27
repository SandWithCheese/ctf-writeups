from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

key = b"f8b8c95092dfbbaee917884d866e4401"
iv = b"e54c750c6a8bd188"

cipher = AES.new(key, AES.MODE_CBC, iv)

with open("projekmatkul-main/libutama.so", "rb") as f:
    libutama = f.read()

flag = cipher.decrypt(libutama)

with open("out.bin", "wb") as f:
    f.write(flag)
