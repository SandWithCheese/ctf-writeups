import hashlib
from string import printable

methods = [
    "md5",
    "sha256",
    "sha3_256",
    "sha3_512",
    "sha3_384",
    "sha1",
    "sha384",
    "sha3_224",
    "sha512",
    "sha224",
]

with open("encrypted_memory.txt", "r") as f:
    enc = eval(f.read())

flag = ""
for i in range(len(enc)):
    for char in printable:
        for method in methods:
            x = (ord(char) + 20) % 130
            x = hashlib.sha512(str(x).encode()).hexdigest()
            x = hashlib.new(method, x.encode()).hexdigest()
            if x == enc[i]:
                flag += char
                break


with open("tipsen_memory.txt", "w") as f:
    f.write(flag)
