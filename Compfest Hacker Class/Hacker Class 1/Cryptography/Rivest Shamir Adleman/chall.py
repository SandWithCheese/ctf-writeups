from Crypto.Util.number import GCD, getStrongPrime, bytes_to_long
from sympy import nextprime
from random import choice
from secret import FLAG
import os

def modeA():
    n = getStrongPrime(1024)
    return n

def modeB():
    e = 3
    return e

def modeC(e):
    while True:
        p = getStrongPrime(1024)
        q = nextprime(nextprime(nextprime(p)))
        if GCD(e, (p-1)*(q-1)) == 1:
            break
    n = p*q
    return n

def setup():
    p = getStrongPrime(1024)
    q = getStrongPrime(1024)
    e = 65537
    return p, q, e

def main():
    print('Starting session.')
    flag = FLAG
    stages = 100
    modes = ['A', 'B', 'C']
    for i in range(stages):
        p, q, e = setup()
        n = p*q
        m = bytes_to_long(os.urandom(32))
        mode = choice(modes)
        if mode == 'A':
            n = modeA()
        elif mode == 'B':
            e = modeB()
        elif mode == 'C':
            n = modeC(e)
        else:
            raise AssertionError('Unknown Mode')

        c = pow(m, e, n)
        print(f'mode = {mode}')
        print(f'n = {n}')
        print(f'e = {e}')
        print(f'c = {c}')

        inp = input("Your answer: ")
        if not inp.isnumeric():
            raise AssertionError('Input is not integer.')
        
        if int(inp) == m:
            print('Correct!')
        else:
            print('Wrong answer!')
            break

    if i == (stages - 1):
        print(f'Congrats! Here\'s your flag: {flag}')
    else:
        print(f'Sorry you have failed at round {i + 1}')
    print('Ending session.')

if __name__ == '__main__':
    try:
        main()
    except:
        print('An error has occured.')