from pwn import *
import json
from Crypto.Util.number import long_to_bytes

host, port = "socket.cryptohack.org", 13374

conn = remote(host, port)
conn.recvline()

conn.sendline('{"option": "get_secret"}')
res = json.loads(conn.recvline())
secret = res["secret"]

conn.sendline('{"option": "sign", "msg":' + f'"{secret}"' + "}")
res = json.loads(conn.recvline())
signature = int(res["signature"], 16)

print(long_to_bytes(signature))

conn.interactive()
