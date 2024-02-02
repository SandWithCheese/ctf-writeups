from pwn import *
import json
from binascii import hexlify

host, port = "socket.cryptohack.org", 13389

conn = remote(host, port)
conn.recvline()

with open("message1.bin", "rb") as f:
    msg = f.read()

msg1 = hexlify(msg).decode()

payload = '{"document":' + f'"{msg1}"' + "}"

conn.sendline(payload)

conn.recvline()
with open("message2.bin", "rb") as f:
    msg = f.read()

msg2 = hexlify(msg).decode()

payload = '{"document":' + f'"{msg2}"' + "}"

conn.sendline(payload)

conn.interactive()
