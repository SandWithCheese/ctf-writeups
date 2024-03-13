from itertools import *


def decrypt(ptxt, key):
    ctxt = b""
    for i in range(len(ptxt)):
        a = ptxt[i]
        b = key[i % len(key)]
        ctxt += bytes([a ^ b])
    return ctxt


random_strs = [
    b"my encryption method",
    b"is absolutely impenetrable",
    b"and you will never",
    b"ever",
    b"ever",
    b"ever",
    b"ever",
    b"ever",
    b"ever",
    b"break it",
]


flag = bytes.fromhex(
    "57657535570c1e1c612b3468106a18492140662d2f5967442a2960684d28017931617b1f3637"
)

perms = list(product([1, 2], repeat=10))

for perm in perms:
    calon_flag = flag
    for i in range(len(perm)):
        for j in range(perm[i]):
            calon_flag = decrypt(calon_flag, random_strs[i])

    # print(decrypt(calon_flag, b"picoCTF"))
    calon_flag = decrypt(calon_flag, b"Africa!")
    if b"picoCTF" in calon_flag:
        print(calon_flag.decode())
        break
