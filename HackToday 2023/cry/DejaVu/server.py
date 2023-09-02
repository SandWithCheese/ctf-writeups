#!/usr/bin/env python3

import time
from secret import get_all_key

import sys


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


def bytes2bin(msg: bytes):
    return bin(int.from_bytes(msg, "big"))[2:]


def bin2bytes(msg: bytes):
    return int(msg, 2).to_bytes((int(msg, 2).bit_length() + 7) >> 3, "big") or b"\x00"


class KeyGen:
    def __init__(self, x: int, m: int, c: int, n: int):
        self.m = m
        self.c = c
        self.n = n
        self.state = x % n
        self.bitstate = bin(self.state)[2:]

    def update_state(self, isflag=0):
        self.state = (self.state * self.m + self.c) % self.n
        self.bitstate = bin(self.state)[2:]
        if isflag:
            return
        time.sleep(1)

    def get_bit(self, isflag=0):
        b = self.bitstate[-1]
        self.bitstate = self.bitstate[:-1]
        if not self.bitstate.isdigit():
            self.update_state(isflag)
        return int(b)


class StreamCipher:
    def __init__(self):
        m, c, n, x = get_all_key()
        self.keygen = KeyGen(x, m, c, n)

    def encrypt(self, msg: bytes, isflag=0):
        return bin2bytes(
            "".join([str(int(b) ^ self.keygen.get_bit(isflag)) for b in bytes2bin(msg)])
        )


def menu():
    print("""[1] Encrypt a message\n[2] Get an encrypted flag\n[3] Exit""")


def main():
    cipher = StreamCipher()
    with open("flag.txt", "rb") as f:
        fl4g = f.read()
        f.close()
    enc_fl4g = cipher.encrypt(fl4g, 1)
    print("Welcome!")
    start = time.time()
    while start - time.time() <= 10:
        menu()
        opcode = input("[>] ").strip()
        if opcode == "3":
            break
        elif opcode == "1":
            msg = input("Message to encrypt : ").strip().encode()
            ct = cipher.encrypt(msg)
        elif opcode == "2":
            msg = "flag"
            ct = enc_fl4g
        else:
            print("Maksud?")
            continue
        if len(msg) == 0:
            print("Invalid message.")
            continue
        print("Encrypted message :", ct.hex())
    return 0


if __name__ == "__main__":
    main()
