from pwn import *
from hashlib import md5
from string import ascii_letters
import itertools
import gmpy2
from Crypto.Util.number import getPrime
from multiprocessing import Pool


host, port = "mercury.picoctf.net", 27379


def get_p(n, e):
    dp_range = range(1, 1 << 20)
    m = getPrime(20)
    for dp in dp_range:
        if dp % 10_000 == 0:
            print(f"[*] Processing {dp}")
        p = gmpy2.gcd(m - pow(m, e * dp, n), n)
        if p > 1:
            print(dp)
            break
    return p


if __name__ == "__main__":
    conn = remote(host, port)

    line = conn.recvline()

    vals1 = line.split()[6].decode()[1:-1]
    print(vals1)

    vals2 = line.split()[-1].decode().strip()
    print(vals2)

    found = False
    candidate = 0
    while not found:
        for i in range(10):
            for c in itertools.combinations_with_replacement(ascii_letters, i):
                payload = vals1 + "".join(c)
                if md5(payload.encode()).hexdigest()[-6:] == vals2:
                    print(payload)
                    found = True
                    break
            if found:
                break

    conn.sendline(payload.encode())

    n = int(conn.recvline().split()[-1].decode())
    e = int(conn.recvline().split()[-1].decode())

    with Pool(5) as pool:
        p = pool.apply_async(get_p, (n, e))
        q = pool.apply_async(get_p, (n, e))
        p = p.get()
        q = q.get()

    q = n // p
    print(p * q == n)

    conn.sendline(str(p + q).encode())

    conn.interactive()
