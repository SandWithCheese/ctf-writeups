import pwn
from gmpy2 import iroot

host = "34.101.174.85"
port = 10004


def isqrt(n):
    x = n
    y = (x + n // x) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def fermat(n):
    t0 = isqrt(n) + 1
    counter = 0
    t = t0 + counter
    temp = isqrt((t * t) - n)
    while (temp * temp) != ((t * t) - n):
        counter += 1
        t = t0 + counter
        temp = isqrt((t * t) - n)
    s = temp
    p = t + s
    q = t - s
    return p, q


def small_e(n, e, c):
    i = 0
    while True:
        m, isRoot = iroot(c + i * n, e)
        if isRoot:
            return m

        i += 1


conn = pwn.remote(host, port)
conn.recvline()

for i in range(1, 101):
    print(i)
    mode = conn.recvline().split()[2].strip().decode()
    n = int(conn.recvline().split()[2].strip().decode())
    e = int(conn.recvline().split()[2].strip().decode())
    c = int(conn.recvline().split()[2].strip().decode())
    conn.recvuntil(b"answer: ")

    if mode == "A":
        phi = n - 1
        d = pow(e, -1, phi)
        m = pow(c, d, n)
        conn.sendline(str(m).encode())
    elif mode == "B":
        m = small_e(n, e, c)
        conn.sendline(str(m).encode())
    elif mode == "C":
        p, q = fermat(n)
        phi = (p - 1) * (q - 1)
        d = pow(e, -1, phi)
        m = pow(c, d, n)
        conn.sendline(str(m).encode())

    conn.recvline()

conn.interactive()
