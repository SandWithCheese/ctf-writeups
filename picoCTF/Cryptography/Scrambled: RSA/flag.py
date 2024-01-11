from pwn import *
from string import ascii_letters, digits

printable = "picoCTF{bad}" + digits + "_" + "abcdef"

host, port = "mercury.picoctf.net", 47987

conn = remote(host, port)

flag = conn.recvline().split()[-1]
n = int(conn.recvline().split()[-1].decode())
e = int(conn.recvline().split()[-1].decode())

BLOCK_SIZE = 308
real_flag = ""
blocks = []
while True:
    for char in printable:
        print(f"[*] Processing {char}")
        payload = real_flag + char
        conn.recvuntil(b"me: ")
        conn.sendline(payload.encode())
        temp = conn.recvline().split()[-1]

        if blocks == []:
            blocks = [temp]
        else:
            for i in blocks:
                temp = temp.replace(i, b"")
            blocks.append(temp)

        if temp in flag:
            real_flag += char
            flag = flag.replace(temp, b"")
            print(real_flag)
            break

    if flag == temp:
        break


conn.interactive()
