from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import pwn

conn = pwn.remote("ctf-gemastik.ub.ac.id", 10002)


def recv_menu():
    conn.recvuntil(b"> ")


def get_cipher():
    ciphertext = int(conn.recvline().decode().strip().split()[2])
    return ciphertext


recv_menu()
conn.sendline(b"2")
flag = long_to_bytes(get_cipher())


recv_menu()
conn.sendline(b"1")
conn.recvuntil(b"plaintext = ")
payload = "AA" * 16 * 7
real_payload = pad(bytes.fromhex(payload), AES.block_size)
payload = bytes_to_long(bytes.fromhex(payload))
conn.sendline(str(payload).encode())
cipher = long_to_bytes(get_cipher())


Os = []
secret = b""
for i in range(0, len(cipher), 16):
    block_payload = real_payload[i : i + 16]
    block_cipher = cipher[i : i + 16]
    block_flag = flag[i : i + 16]

    o = bytes_to_long(block_payload) ^ bytes_to_long(block_cipher)
    Os.append(o)

    temp = bytes_to_long(block_flag) ^ o
    secret += long_to_bytes(temp)

recv_menu()
conn.sendline(b"3")
conn.recvuntil(b"secret: ")
conn.sendline(str(bytes_to_long(secret)).encode())
flag = conn.recvline().decode().strip()
conn.close()
print(flag)
