from pwn import *


def bytes2matrix(text):
    return [list(text[i : i + 4]) for i in range(0, len(text), 4)]


def matrix2bytes(matrix):
    return bytes(sum(matrix, []))


def hex2matrix(text):
    return bytes2matrix(bytes.fromhex(text))


def encrypt_msg(msg: bytes):
    conn.sendlineafter(b"> ", b"1")
    conn.sendlineafter(b": ", msg)
    return conn.recvline().strip().decode().split(" : ")[1]


host, port = "157.230.251.184", "10013"

conn = remote(host, port)

conn.recvuntil(b"reason")
conn.recvline()
conn.recvline()

flag = conn.recvline().strip().decode().split(" : ")[1]
print(f"Flag: {flag}")

print(hex2matrix(flag[:32]))
print(hex2matrix(encrypt_msg(b"a")))

conn.interactive()
