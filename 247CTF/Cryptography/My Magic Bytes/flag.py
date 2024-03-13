from pwn import xor

with open("my_magic_bytes.jpg.enc", "rb") as f:
    datas = f.read()
    # print(datas)

# magic_bytes = datas[0]
jpg_header = b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00\x01"
result = xor(datas, jpg_header)
key = result[: len(jpg_header)]
flag = xor(datas, key)

with open("flag1.jpg", "wb") as f:
    f.write(datas)
# print(flag)
# print(jpg_header)
