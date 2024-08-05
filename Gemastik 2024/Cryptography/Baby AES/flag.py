#!/usr/local/bin/python

from pwn import *
from binascii import unhexlify, hexlify
from string import ascii_uppercase, ascii_lowercase, digits
from itertools import product
from tqdm import tqdm

printable = ascii_uppercase + ascii_lowercase + digits + "_{}"

host, port = "ctf.gemastik.id", "10004"

conn = remote(host, port)

conn.recvline()
conn.recvline()

enc = conn.recvline().strip().split(b": ")[1]


iv, enc_flag = enc[:32], enc[32:]
last_block = enc_flag[-32:]

real_flag = b""
check_cipher = b""

for prod in tqdm(product(printable, repeat=2)):
    flag = "".join(prod).encode() + b"}"
    conn.sendlineafter(b"message: ", hexlify(flag))
    tmp_enc = conn.recvline().strip().split(b": ")[1]
    tmp_iv, tmp_enc_flag = tmp_enc[:32], tmp_enc[32:]
    tmp_imm = xor(unhexlify(tmp_enc_flag[:32]), unhexlify(tmp_iv))
    test_cipher = xor(tmp_imm, unhexlify(last_block))

    try:
        test_flag = test_cipher.decode()
        real_flag += test_cipher + flag
        check_cipher = test_cipher
        break
    except:
        pass

i = 2
while len(real_flag) != 67:
    conn.sendlineafter(b"message: ", hexlify(check_cipher))
    tmp_enc = conn.recvline().strip().split(b": ")[1]
    tmp_iv, tmp_enc_flag = tmp_enc[:32], tmp_enc[32:]
    tmp_imm = xor(unhexlify(tmp_enc_flag[:32]), unhexlify(tmp_iv))
    test_cipher = xor(tmp_imm, unhexlify(enc_flag[-32 * i : -32 * (i - 1)]))

    real_flag = test_cipher + real_flag

    check_cipher = test_cipher

    i += 1

print(real_flag.decode())
