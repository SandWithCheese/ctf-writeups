from pwn import *
from string import ascii_uppercase, digits
from itertools import combinations

possible_char = ascii_uppercase + digits

local = False
if local:
    p = process("./soal")
else:
    p = remote("34.101.174.85", 10003)

serial_list = combinations(possible_char, 20)
count = 0
for serial in serial_list:
    payload = "-".join(list("".join(list(serial[i : i + 4])) for i in range(0, 20, 4)))
    p.sendline(payload.encode())

    if count == 100:
        break
    count += 1

p.interactive()
