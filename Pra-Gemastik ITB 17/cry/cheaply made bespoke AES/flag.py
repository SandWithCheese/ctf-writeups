from pwn import *
from string import printable
from binascii import hexlify

host, port = "4.145.98.52", 8010

flag_char = b"CTFITB{wh4t_a_ch3ap5kat3_1t5_n0t_ev3n_th4t_3xpen51"
flag = hexlify(flag_char)

context.log_level = "error"

while flag == b"" or flag[-1] != b"}":
    for char in printable:
        conn = remote(host, port)
        conn.recvuntil(b"m: ")
        conn.sendline(flag + hexlify(char.encode()))

        print(f"Trying {char}")
        c = conn.recvline().strip().split(b": ")[1]

        ct = conn.recvline().strip().split(b": ")[1]

        if c[: len(flag) + 2] == ct[: len(flag) + 2]:
            flag += hexlify(char.encode())
            flag_char += char.encode()
            print(f"Flag: {flag_char.decode()}")
            break

        conn.close()


conn.interactive()
