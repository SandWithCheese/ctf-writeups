from pwn import *

host, port = "157.230.251.184", "10011"

conn = remote(host, port)


for i in range(256):
    print(f"i: {i}")
    for j in range(256):
        payload = hex(i)[2:] + hex(j)[2:]
        conn.sendlineafter(b"anda: ", payload.encode())
        flag = conn.recvline()
        if b"slashroot" in flag:
            print(flag)
            exit()

conn.interactive()
