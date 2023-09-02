from Crypto.Util.number import *
from functools import reduce
import random

def secure_padding(plain,length):
    return plain + b"\x00" * (length - len(plain))

def get_public_key(BIT,size):
    list_primes = [getPrime(BIT) for _ in range(size)]
    n = reduce(lambda x,y : x*y,list_primes)
    return n, list_primes

def read_file(path):
    with open(path,"rb") as f:
        content = f.read().strip()
        f.close()
    return content

def main():
    size = 10
    BIT = 1024  
    e = 0x10001
    flag = read_file("flag.txt")

    assert len(flag) < (BIT//8)

    flag = secure_padding(flag,(BIT//8) + random.randint(10000,100000))

    m = bytes_to_long(flag)    
    n, list_primes = get_public_key(BIT,size)
    c = pow(m,e,n)

    gift = list_primes[random.randint(0, size - 1)]

    print(f"{n = }")
    print(f"{e = }")
    print(f"{c = }")
    print(f"{gift = }")
    

if __name__ == "__main__":
    main()