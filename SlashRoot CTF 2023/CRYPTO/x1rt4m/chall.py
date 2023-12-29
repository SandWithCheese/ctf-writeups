from binascii import hexlify
from secret import flag

import string
import random
import numpy as np

def xor(a, b):
    return [ord(x)^y for x,y in zip(a,b)]

def pad(text):
    padding_len = 16 - (len(text) % 16)
    return text + bytes([padding_len]) * padding_len

def t2m(s,r,c):
    if len(s) != (r * c):
        print("Incorect Matrix Size!")
        exit()

    ascii_values = np.zeros(len(s), dtype=int)

    for i, char in enumerate(s):
        ascii_values[i] = ord(char)

    matrix = np.reshape(ascii_values, (r, c))

    return matrix

def encrypt(plaintext, key, iv):
    ciphertext = []
    a = np.dot(plaintext.T, key)
    pt = [ j for i in a.tolist() for j in i]
    
    pt_block = [pt[i:i+16] for i in range(0,len(pt),16)]
    init = iv
    
    for block in pt_block:
        ciphertext_block = init
        result = xor(ciphertext_block, block)
        ciphertext.append(result)
        init = ciphertext_block
    
    return [j for i in ciphertext for j in i]

key = ''.join(i for i in random.choices(string.ascii_uppercase, k=4))
IV = list(pad(flag[:11].encode('latin1')).decode()) # are u lucky enough to guess the IV? well i doubt it hahahaha
key2matrix = t2m(key,2,len(key)//2)
flag2matrix = t2m(hexlify(pad(flag.encode('latin1'))).decode(),2,len(hexlify(pad(flag.encode('latin1'))).decode())//2)

print(f"ciphertext : {encrypt(flag2matrix,key2matrix,IV)}") 