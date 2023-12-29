from pwn import *

ciphertext = bytes.fromhex("2e0c010d46000048074900090b191f0d484923091f491004091a1648071d070d081d1a070848")
plaintext = "Here is a sample. Pay close attention!"

# print(xor(ciphertext, plaintext))
key = "fish"
flag = bytes.fromhex("0005120f1d111c1a3900003712011637080c0437070c0015")
print(xor(key, flag))