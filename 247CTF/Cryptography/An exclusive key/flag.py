from pwn import xor

with open("exclusive_key", "rb") as f:
    data = f.read()

# flag_format = b"247CTF{"
# flag = xor(data, flag_format)
# print(flag[:40])

key = b'<!DOCTYPE html>\n<html class="client-nojs"> <body>'
flag = xor(data, key)
print(flag[:40].decode())

# flag_format = b"247CTF{cb82a>1bb9o4654e195v6ccec2'48f47}"
# flag = xor(data, flag_format)
# print(flag[:40])
