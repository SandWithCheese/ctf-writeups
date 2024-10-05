from pwn import *
from Crypto.Util.Padding import pad

host, port = "challenges.ctf.compfest.id", "20016"


def send_option(option: str):
    conn.sendlineafter(b">> ", option.encode())


def send_message(message: str):
    conn.sendlineafter(b"Message: ", message.encode())


def get_encrypted_message():
    conn.recvuntil(b"Encrypted Message (hex): ")
    return conn.recvline().strip()


conn = remote(host, port)

send_option("2")
enc_flag = get_encrypted_message()

flag = ""

i = 0
while "}" not in flag:
    send_option("1")
    send_message(flag)

    message_last_block = get_encrypted_message().decode()[-32:]

    intermediate_value = xor(bytes.fromhex(message_last_block), pad(b"", 16))

    assert len(intermediate_value) == 16

    flag_block = bytes.fromhex(enc_flag.decode())[i * 16 : (i + 1) * 16]

    flag += xor(intermediate_value, flag_block).decode()

    i += 1

print(flag)
