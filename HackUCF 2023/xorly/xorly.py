#!/usr/bin/env python2

def encrypt(plaintext, key):

    ciphertext = []
    for i in range(0, len(plaintext)):
        ciphertext.append(ord(plaintext[i]) ^ ord(key[i%len(key)])) 

    return ''.join(map(chr, ciphertext))

decrypt = encrypt

'''
I'll give you a sample of how this works:

Plaintext: 
"Here is a sample. Pay close attention!"

Ciphertext: (encoded in hex)
2e0c010d46000048074900090b191f0d484923091f491004091a1648071d070d081d1a070848

Flag: (encoded in hex, encrypted with the same key)
0005120f1d111c1a3900003712011637080c0437070c0015
'''
