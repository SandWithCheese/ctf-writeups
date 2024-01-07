from pwn import *
import z3
from Crypto.Util.number import long_to_bytes

host, port = "103.127.99.15", 5000

conn = remote(host, port)
for i in range(30):
    print("[*] Solving challenge", i + 1)
    n = int(conn.recvline().split(b"=")[1])
    e = int(conn.recvline().split(b"=")[1])
    c = int(conn.recvline().split(b"=")[1])
    ppq = int(conn.recvline().split(b"=")[1])

    p = z3.Int("p")
    q = z3.Int("q")

    s = z3.Solver()
    s.add(p + q == ppq)
    s.add(p * q == n)

    s.check()
    m = s.model()
    p = m[p].as_long()
    q = m[q].as_long()

    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = pow(c, d, n)
    m = long_to_bytes(m)

    conn.recvuntil(b"> ")
    conn.sendline(m)
    conn.recvline()

conn.interactive()
