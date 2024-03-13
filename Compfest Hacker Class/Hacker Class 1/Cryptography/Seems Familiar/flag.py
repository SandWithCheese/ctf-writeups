import pwn
from string import printable
from Crypto.Util.Padding import pad
import binascii

printable_hex = []
for char in printable:
    printable_hex.append(binascii.hexlify(char.encode()))

print(printable_hex)

host = "34.101.174.85"
port = 10000

conn = pwn.remote(host, port)


def get_encrypted(payload: bytes):
    conn.recvuntil(b"Exit\n")
    conn.sendline(b"2")
    conn.recvuntil(b"= ")
    conn.sendline(payload)
    encrypted = conn.recvline().split()[3].decode()
    return encrypted


# flag = get_encrypted(b"")
# print(flag)

# pad = 5
# for i in range(16):
#     flag = get_encrypted(b"AA" * i)
#     if len(flag) > 160:
#         pad = i
#         break


payload = b"dd2f3f203a7ee5055bbadb15302b9c1b81b78a747901fd3232dbd9ff479495}"
for i in range(48 + 16, 64 + 16):
    for char_hex in printable_hex:
        print(f"{i}: {char_hex}")
        flag_last_block = get_encrypted(b"AA" * (4 + i))[-96 - 32 - 32 : -64 - 32 - 32]
        test = pad(binascii.unhexlify(char_hex + binascii.hexlify(payload)), 16)
        test = binascii.hexlify(test)
        print(test)
        payload_first_block = get_encrypted(test)[:32]
        if flag_last_block == payload_first_block:
            print("Found")
            payload = binascii.unhexlify(char_hex) + payload
            break

print(payload)
# print(get_encrypted(b"AA" * 32))
# print(get_encrypted(b"AABB" * 16))


# conn.interactive()
