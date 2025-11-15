#!/usr/bin/env python3

import signal, os
from Pailier import *
from Crypto.Util.number import *

signal.alarm(50)

with open("/flag.txt", "rb") as f:
    flag_bytes = f.read()

key = os.urandom(66)              
key_int = bytes_to_long(key)

cipher = pailier()

while True:
    print("1. encrypt")
    print("2. bingo")
    print("3. decrypt")
    print("4. key?")
    inp = int(input("> "))

    if inp == 1:
        print("pt (hex)")
        inp = input("> ")
        ct = cipher.encrypt(int(inp, 16))
        print('ct : ', '{0:x}'.format(ct))

    elif inp == 2:
        print("key (hex)")
        user_hex = input("> ").strip()
        try:
            user_key = bytes.fromhex(user_hex)
        except Exception:
            print("nope")
            continue

        if len(user_key) == 66 and user_key == key:
            try:
                print(flag_bytes.decode())
            except Exception:
                print(flag_bytes.hex())
        else:
            print("nope")

    elif inp == 3:
        print("ct (hex)")
        inp = input("> ")
        pt = cipher.decrypt(int(inp, 16))
        print('pt : ', '{0:x}'.format(pt))

    elif inp == 4:
        ct = cipher.encrypt(key_int)
        print('ct : ', '{0:x}'.format(ct))

    else:
        exit()
