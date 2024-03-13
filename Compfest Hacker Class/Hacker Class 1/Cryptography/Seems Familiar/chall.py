from ast import Assert
import sys
import os
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from secret import FLAG

IV = os.urandom(AES.block_size)
KEY = os.urandom(AES.block_size)

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

def get_flag():
    print("Sorry, the get_flag function is currently broken. Please try something else.")

def encrypt(msg = None):
    if msg == None:
        msg = input("message (in hex) = ")
    assert len(msg) % 2 == 0, f"Invalid Odd-length string of {msg} has been inputted."
    try:
        msg = binascii.unhexlify(msg.encode()) + FLAG
    except:
        raise AssertionError(f"{msg} is not a valid hex representation.")
    enc = AES.new(KEY, AES.MODE_ECB)
    cipher = enc.encrypt(pad(msg, 16))
    print("ciphertext (in hex): " + binascii.hexlify(cipher).decode())

#DEPRECATED
def decrypt():
    print("Sorry, the decrypt function is currently broken. Please try something else.")

def menu():
    print("1. Get encrypted flag")
    print("2. Encrypt a message")
    print("3. Decrypt a message")
    print("4. Exit")

def main():
    try:
        while True:
            menu()
            choice = input("> " )
            if choice == "1":
                get_flag()
            elif (choice == "2"):
                encrypt()
            elif (choice == "3"):
                decrypt()
            elif (choice == "4"):
                print("ending session.")
                break
            else:
                print("invalid input.")
    except Exception as e:
        print(repr(e))

if __name__ == "__main__":
    main()
