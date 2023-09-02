from pwn import *
from primefac import primefac
from Crypto.Util.number import long_to_bytes

host, port = "103.181.183.216", 18001

e = 65537

conn = remote(host, port)

pairs = []
d = conn.recvuntil(b"Input").split(b"\n")[:-1]
pair = []
for item in d:
    if b"n" in item or b"c" in item:
        pair.append(int(item.decode().split()[2]))
    if len(pair) == 2:
        pairs.append(pair)
        pair = []

pairs = reversed(pairs)

for pair in pairs:
    p, q = list(primefac(pair[0]))
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = pow(pair[1], d, pair[0])
    print(long_to_bytes(m))


conn.interactive()
