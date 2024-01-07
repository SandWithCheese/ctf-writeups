from binascii import hexlify, unhexlify
from os import urandom, popen
from Crypto.Util.number import long_to_bytes, bytes_to_long
from flag import flag
import signal

def h(x, n):
    return (x >> (n * 8)) & 0xff

def g(x, y, z):
    res = (3*x + 5*y + 7*z) % 0x100
    return ((res << 4) | (res >> 4)) & 0xff

def f(x, key):
    x ^= key
    out_0 = g(h(x, 0), h(x, 1), 0)
    out_1 = g(h(x, 2), h(x, 1) ^ out_0, 1)
    out_2 = g(h(x, 2) ^ out_1, h(x, 3), 0)
    out_3 = g(h(x, 3), h(x, 3), 1)

    return ((out_3 << 24) | (out_2 << 16) | (out_1 << 8) | (out_0))

def cipher(pt, keys):
    left, right = pt >> 32 & 0xffffffff, pt & 0xffffffff
    
    left, right = left, right ^ left
    num_round = 4
    for i in range(num_round):
        left, right = left ^ f(right, keys[i]), right
        if i == num_round - 1:
            break
        left, right = right, left
    left, right = left, right ^ left

    assert left < 2 ** 32
    assert right < 2 ** 32
    return ((left << 32) | (right))

def pad(msg):
    return msg + chr(8 - len(msg) % 8).encode() * (8 - len(msg) % 8)

def encrypt(msg, keys):
    encrypted = b''
    enc_keys = [keys[0], keys[1], keys[2], keys[3]]
    msg = pad(msg)
    for i in range(len(msg) // 8):
        encrypted += long_to_bytes(cipher(bytes_to_long(msg[8 * i:8 * (i + 1)]), enc_keys))
    return encrypted

def decrypt(msg, keys):
    decrypted = b''
    dec_keys = [keys[3], keys[2], keys[1], keys[0]]
    for i in range(len(msg) // 8):
        decrypted += long_to_bytes(cipher(bytes_to_long(msg[8 * i:8 * (i + 1)]), dec_keys))
    return decrypted

def print_menu():
    print('1. Encrypt something')
    print('2. Encrypt flag')

if __name__ == '__main__':
    signal.alarm(30)
    
    keys = [bytes_to_long(urandom(4)) for _ in range(4)]
    flag = flag.encode()
    
    try:
        while True:
            print_menu()
            choice = input('> ').strip()
            if choice == '1':
                msg = unhexlify(input('message (hex): '))
                enc = encrypt(msg, keys)
                dec = decrypt(enc, keys)
                assert pad(msg) == dec
                enc = enc[:8] # one block only hehe
                print(hexlify(enc).decode())
            elif choice == '2':
                enc = encrypt(flag, keys)
                dec = decrypt(enc, keys)
                assert pad(flag) == dec
                print(hexlify(enc).decode())
            else:
                print('Bye.')
                break
    except:
        print('Error.')