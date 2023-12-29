from Crypto.Cipher import AES
from Crypto.Util.Padding import *
import string
import random
import os
from Crypto.Util.number import *
from secrets import FLAG, enc

def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def encrypt(msg,key,iv):
###############################################################################
#                                                                             #
#                    Haduh kena prank opo iki rek jadi ilang                  #
#                   Seinget gw ini AES jg deh cm entah apa ini                #
#                              Gudlak All!! :)                                #
#                                                                             #
###############################################################################
    return enc.hex()

key = os.urandom(16)
iv1 = os.urandom(16)
iv2 = os.urandom(16)
plainkey = os.urandom(16)

enckey = encrypt(plainkey + os.urandom(16), key, iv1)

code = ("Very simple, " + generate_random_string(random.randint(50,60))).encode()

cipher = AES.new(plainkey + (os.urandom(2)*8),AES.MODE_CBC, iv2)

enccode = cipher.encrypt(pad(code,16))

print(f'enckey = {enckey}')
print(f'enccode = {enccode}')
print(f'iv2 = {iv2}')

while True:
    print("""      ========================================
        1. Tes Enkripsi
        2. Tebak kode
        3. Exit
        ============================================""")

    choose = input(">> ")
    if choose == "1":
        plaintext = input("Masukan pesan: ")
        try:
            plaintext = bytes.fromhex(plaintext)
            ciphertext = encrypt(plaintext, key, iv1)
            print(f'Ciphertext = {ciphertext}')
        except:
            print("woila...")

    elif choose == "2":
        cobaan = input("Masukkan kode: ").encode()
        if cobaan == code:
            print(f'dahlah, {FLAG}')
            exit(1)
        else:
            print("salah :(")
            exit(0)

    elif choose == "3":
        print("Bye!")
        exit(1)
            
    else:
        print("woi!")
        exit(0)