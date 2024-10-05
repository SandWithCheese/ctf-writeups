#!/usr/bin/env python3

import aes
import os
# from secret import flag
flag = b"flag{this_is_a_fake_flag}"
from binascii import hexlify

KEY = os.urandom(16)

def encrypt(key,s):
    cipher = aes.AES(key)
    s_block = aes.split_blocks(aes.pad(s))
    ct = ''.join(i for i in [hexlify(cipher.encrypt_block(i)).decode() for i in s_block])

    return ct

def decrypt():
    return None

def main():
    flag_enc = encrypt(KEY, flag)

    banner = """
   _____         ______  _____ 
  / ____|  /\   |  ____|/ ____|
 | (___   /  \  | |__  | (___  
  \___ \ / /\ \ |  __|  \___ \ 
  ____) / ____ \| |____ ____) |
 |_____/_/    \_\______|_____/ 
                               
                               
"""

    menu = f"""
Welcome to my secure AES algorithm
you are not allowed to use your own key for security reason

flag : {flag_enc}

[1] Encrypt Msg
[2] Decrypt Msg
[3] Exit
"""

    print(banner)
    print(menu)

    while True:

        user_input = int(input("> "))

        if user_input == 1:
            user_pt = input("Msg to Encrypt : " ).encode("latin-1")
            user_ct = encrypt(KEY,user_pt)
            print(f"Your encrypted msg is : {user_ct}\n")
        elif user_input == 2:
            print("Under construction, please try again later\n")
        elif user_input == 3:
            print("Bye-Bye!")
            exit()
        else:
            print("Input Invalid!\n")

if __name__ == "__main__":
    main()