from pwn import *
from hashlib import md5
from string import ascii_letters
import itertools

host, port = "mercury.picoctf.net", 27379

conn = remote(host, port)

line = conn.recvline()
# print(line)

vals1 = line.split()[6].decode()[1:-1]
print(vals1)

vals2 = line.split()[-1].decode().strip()
print(vals2)

found = False
candidate = 0
while not found:
    # # payload = vals1
    # for char in printable:
    #     payload = vals1 + char
    #     print(payload)
    #     hashed = md5(payload.encode()).hexdigest()[-6:]
    #     print(hashed) 
    #     if hashed == vals2:
    #         found = True
    #         print(payload)
    #         break
    
    # vals1 += printable[0]
    # payload = vals1 + str(candidate)
    # hashed = str(md5(payload.encode()).hexdigest()[-6:])
    # print(hashed)
    # if hashed == vals2:
    #     print(payload)
    #     found = True
    #     break
    # candidate += 1
    for c in itertools.combinations_with_replacement(ascii_letters, 5):
        payload = vals1 + "".join(c)
        print("".join(c))
        if md5(payload.encode()).hexdigest()[-6] == vals2:
            print(payload)
            found = True
            break


conn.interactive()