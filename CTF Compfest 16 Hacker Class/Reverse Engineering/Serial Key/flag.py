from pwn import *
from itertools import combinations

valid_chars = "ABDEGHIJKLMNOPQRSTUVWXYZ02345789"

host, port = "challenges.ctf.compfest.id", "20012"

conn = remote(host, port)

i = 0
for comb in combinations(valid_chars, 16):
    if i == 100:
        break

    combi = "".join(comb)
    payload = f"{combi[:4]}-{combi[4:8]}-CF16-{combi[8:12]}-{combi[12:]}"

    conn.sendlineafter(b"==> ", payload.encode())
    i += 1

conn.interactive()
