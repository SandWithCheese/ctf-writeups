from pwn import *
import json
import base64
import codecs
from Crypto.Util.number import long_to_bytes

host, port = "socket.cryptohack.org", 13377

conn = remote(host, port)
for i in range(100):
    log.info(f"Round {i}")
    res = conn.recvline()
    res = json.loads(res)
    t = res["type"]
    encoded = res["encoded"]
    if t == "base64":
        decoded = base64.b64decode(encoded).decode()
    elif t == "hex":
        decoded = bytes.fromhex(encoded).decode()
    elif t == "rot13":
        decoded = codecs.decode(encoded, "rot_13")
    elif t == "bigint":
        decoded = long_to_bytes(int(encoded, 16)).decode()
    elif t == "utf-8":
        decoded = "".join([chr(b) for b in encoded])

    payload = '{"decoded": "' + decoded + '"}'
    conn.sendline(payload)

conn.interactive()
