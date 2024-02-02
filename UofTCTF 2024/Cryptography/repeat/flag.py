from binascii import unhexlify

enc_flag = "982a9290d6d4bf88957586bbdcda8681de33c796c691bb9fde1a83d582c886988375838aead0e8c7dc2bc3d7cd97a4"

flag_part = "uoftctf{"

key = ""
for i in range(len(flag_part)):
    key += chr(ord(flag_part[i]) ^ int(enc_flag[i * 2 : i * 2 + 2], 16))

enc_flag = unhexlify(enc_flag)

flag = ""
for i in range(len(enc_flag)):
    flag += chr(ord(key[i % len(key)]) ^ enc_flag[i])

print(flag)
