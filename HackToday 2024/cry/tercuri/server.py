from Crypto.Util.number import *
from secrets import choice 

with open('tersangka.txt','r') as f:
    TERSANGKA = f.read().splitlines()

def enc(m):
    while(True):
        p = getPrime(512)
        q = getPrime(512)
        e = getPrime(5)
        n = p*q
        c = pow(m,e,n)
        phi = (p-1)*(q-1)
        if GCD(e, phi) == 1:
            return n,e,c

if __name__ == '__main__':
    tt = choice(TERSANGKA)
    tersangka = bytes_to_long(tt.encode())
    n,e,c = enc(tersangka)

    print(f'{n = }')
    print(f'{e = }')
    print(f'{c = }')