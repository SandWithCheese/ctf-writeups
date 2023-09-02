from pwn import *

possible_letters = "BCDEHIKOSXZ"

host, port = "103.181.183.216", 19001

conn = remote(host, port)

text = conn.recvline().decode().strip()

possible_passes = []
pwd = ""
for char in text:
    if char not in possible_letters and pwd != "":
        if len(pwd) > 12:
            possible_passes.append(pwd)
        pwd = ""
    else:
        pwd += char
print(possible_passes)

conn.interactive()
