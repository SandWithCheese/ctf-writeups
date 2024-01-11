from pwn import *
from Crypto.Util.number import long_to_bytes

# from sympy.ntheory import factorint

host, port = "saturn.picoctf.net", 56994

conn = remote(host, port)

c = int(conn.recvline().strip().split(b"=")[-1])
d = int(conn.recvline().strip().split(b"=")[-1])
e = 65537

# d = e^-1 mod (p-1)(q-1)
# ed = 1 mod (p-1)(q-1)
# ed - 1 = k(p-1)(q-1)
kphi = d * e - 1
# factors = factorint(kphi)

print(long_to_bytes(pow(c, d, kphi)))

conn.interactive()
