import base64
from function import *
from hashlib import sha256
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES


def deconvert(enc):
    i = 0
    while True:
        try:
            enc = int(enc, 16)
            return enc, i
        except:
            enc = base64.b64decode(enc).decode()
            i += 1


with open("output.txt", "r") as f:
    p = f.readline().strip().split(" = ")[1]
    g = f.readline().strip().split(" = ")[1]
    A = f.readline().strip().split(" = ")[1]
    B = f.readline().strip().split(" = ")[1]
    # c = f.readline().strip().split(" = ")[1]
    c = b"\xa1\xb267\x9aA\xb3\xda\xba\x92\x08\xaf\x11\x88[\xf2\x7fyxC\x15\xe1\x95\xee\xdd\x171lx#q^L\x94-\x9e;/\x92\x9cq9J\xac\xda\xc1\x88\x15\x7f<\xab\x95\xbe\x98\xda\xc8\xa6\x8e\xd5[\x1a\xed\xad\xb6=\xcf7]\x17\x01\xd8v\x19\xc4\x89\xc8[\xda\xb87\x1b\xbaA\x1e=\x87\x94z\x15\xc8\xea[LA\x1d~:\x90\xc0\xeac\xd0\xf4\xa8*\xa8\x98\xa5\x89B\xdex\x84\xab\xb5S?\xca\xa1o\xd8\x90\x074\x175II}\xd2\x19\x03+\xbd\xe9\xd2X`\xc7\xed\xd4hBdc\x93\xee\xae\x83g\x0e\xd3\x1d@\x0e\xb5\xfb\xebj\xaaG`\xacQ\xc9\xf5\xac7\xf0\xbdP_|\x8a\x1d\x94\xa3w\xe5;H6\xe0Z\xd3\xf7\xbd\xb6\x1a\x9f\x89`+W\xe8|\xdbB\x8b;\xefpE\xd3h\xec\x06\x07E\x89\xd5l\xd1\x00<\xa7\x97\xb2Od\x1ew\x19e\xca\xaf\xf7\xba-NlH\t\xeb\x1ck\x96\xc5`\xe4\\\xb8\x7f0\x0fZf\x18t\rN\x84\x87\x02\xc86"
    z = 16


p, x = deconvert(p)
print(p, x)

g, y = deconvert(g)
print(g, y)

A = int(A, 2)
print(A)

B = int(B, 8)
print(B)

R = IntegerModRing(p)
a = discrete_log(R(A), R(g))
b = discrete_log(R(B), R(g))

print(a)
print(b)

C = pow(A, b, p)
assert C == pow(B, a, p)

iiv = pow(x, y)
iiv = modify_digit(iiv, rules)
print(iiv)

hash = sha256()
hash.update(long_to_bytes(C))

key = hash.digest()[:16]
iv = iiv.to_bytes(z, byteorder="little")
cipher = AES.new(key, AES.MODE_CBC, iv)

decrypt = cipher.decrypt(c)
print(decrypt)
