#!/usr/bin/python3

import os
import sys
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long
from Crypto.Util.Padding import pad

class Unbuffered(object):
  def __init__(self, stream):
    self.stream = stream
  def write(self, data):
    self.stream.write(data)
    self.stream.flush()
  def writelines(self, datas):
    self.stream.writelines(datas)
    self.stream.flush()
  def __getattr__(self, attr):
    return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

with open("flag.txt", "rb") as f:
    flag = f.read()
    f.close()

def encrypt(pt: bytes, iv: bytes, key: bytes):
    aes = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128)
    pt = pt + flag[:len(flag)//2]
    pt = pad(pt, 16)
    ct = aes.encrypt(pt)
    return iv+ct

def generate_key():
    return bin(bytes_to_long(os.urandom(2)))[5:].zfill(16)

def gift(pt : bytes):
    key = generate_key()
    iv = b"hektoday"*2
    assert len(key) == 16 and len(iv) == 16
    print(key)
    aes = AES.new(key.encode(), AES.MODE_CBC, iv=iv)
    return aes.encrypt(pt)

def menu():
    print(
"""[1] Encrypt
[2] Flag
[3] Exit""")


def main():
    key = os.urandom(16)
    for _ in range(4):
        menu()
        op = input("[>] ")
        if op == "1":
            iv = bytes.fromhex(input("[>] IV (hex): "))
            pt = bytes.fromhex(input("[>] Plaintext (hex): "))
            iv = pad(iv, 16) if len(iv) < 0x10 else iv
            pt = pad(pt, 16)
            ct = encrypt(pt, iv, key)
            print("[*] Ciphertext:", ct.hex())
        elif op == "2":  
            print("[*] Encrypted Flag:", gift(gift(flag[16:])).hex())
        elif op == "3":
            break
        else:
            print("[?] Are you drunk?")
        print()

    return 0


if __name__ == "__main__":
    main()