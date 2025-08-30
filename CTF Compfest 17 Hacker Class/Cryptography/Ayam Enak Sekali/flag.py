from pwn import *
from binascii import unhexlify, hexlify

host, port = "ctf.compfest.id", "7103"

conn = remote(host, port)

conn.sendlineafter(b"> ", b"3")

decrypted_flag = conn.recvline().strip().decode()
log.info(f"Decrypted flag: {decrypted_flag}, Length: {len(decrypted_flag)}")

block_size = 32

flag = b""
for i in range(len(decrypted_flag) // block_size):
    block = decrypted_flag[-64 - 32 * (i) :]
    log.info(f"Block: {block}, Length: {len(block)}")
    conn.sendlineafter(b"> ", b"2")
    conn.sendlineafter(b"> ", block.encode())
    flag_part = conn.recvline().strip()
    if b"Tidak bisa" in flag_part:
        break
    flag = flag_part

log.info(f"Flag: {flag}")

conn.close()
