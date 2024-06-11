import binascii
import os
import random

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)

def generate_iv():
    iv = random_with_N_digits(16)
    seed = os.urandom(2)
    seed = int(binascii.hexlify(seed), 16)
    random.seed(seed)
    key = random.randint(0, 9999999999999999)

    return bytes(str(iv^key), 'utf-8')