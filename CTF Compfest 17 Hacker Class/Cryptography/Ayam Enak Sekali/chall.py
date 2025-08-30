from binascii import hexlify, unhexlify
from os import urandom
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = urandom(AES.key_size[0])
FLAG = b"COMPFEST17{REDACTED}"

def encrypt(msg):
    pt = pad(msg, AES.block_size)
    iv = urandom(AES.block_size) 
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pt) 

    return iv + ciphertext

def decrypt(ct):
    iv = ct[:AES.block_size]
    ciphertext_data = ct[AES.block_size:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext_data)
    return unpad(plaintext, AES.block_size)

def print_banner():
    print(r"""
+----------------------------------------------------+
|                                                    |
|           _                                        |
|         >(.)__     🐣 Kandang Ayam Rahasia         |
|          (___/     Sebuah telur misterius          |
|         /    \     telah muncul...                 |
|        /_/|_|\                                     |
|                                                    |
+----------------------------------------------------+
""")


def menu():
    print_banner()
    print('1. Bikin telur')
    print('2. Pecahin telur')
    print('3. Dapat telur rahasia')
    print('4. Keluar dari dapur')

while True:
    try:
        menu()
        choice = input('> ')
        if choice == '1':
            pt = input('> ')
            print(hexlify(encrypt(pt.encode())).decode())
        elif (choice == '2'):
            ct = unhexlify(input('> '))
            if decrypt(ct) == FLAG:
                print("Tidak bisa memecahkan telur ini!")
            else:
                print(decrypt(ct))
        elif (choice == '3'):
            print(hexlify(encrypt(FLAG)).decode())
        elif (choice == '4'):
            print('Bye.')
            break
        else:
            print('Invalid input!')
    except:
        print("Oops mesin pemecah telur rusak")