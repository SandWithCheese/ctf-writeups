import pwn
from Crypto.Util.number import long_to_bytes, bytes_to_long
import sys
import string

chars = string.ascii_letters + string.digits + "_-\{\}"
# print(chars)

sys.set_int_max_str_digits(10_000)


conn = pwn.remote("mercury.picoctf.net", 47987)
flag = int(conn.recvline().decode().strip().split()[1])
n = int(conn.recvline().decode().strip().split()[1])
e = int(conn.recvline().decode().strip().split()[1])

flag = str(flag)


def get_cipher():
    return int(conn.recvline().decode().strip().split()[3])


block_flag = []
for i in range(0, len(flag), 308):
    block = flag[i : i + 308]
    block_flag.append(block)

# print(len(block_flag))

# print(bytes(chars[0], "utf-8"))


shifted_flag = b""
known = []
while len(block_flag) > 0:
    for char in chars:
        print(char)
        conn.recvuntil(b"me: ")
        payload = shifted_flag + bytes(char, "utf-8")
        conn.sendline(payload)
        cipher = str(get_cipher())

        for blocks in known:
            cipher = cipher.replace(blocks, "")

        if cipher in block_flag:
            print("Found")
            shifted_flag += bytes(char, "utf-8")
            known.append(cipher)
            block_flag.remove(cipher)
            break
    print(f"{shifted_flag=}")

print(shifted_flag)


# conn.interactive()
