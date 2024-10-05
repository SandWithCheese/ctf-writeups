from ecdsa import ellipticcurve
from Crypto.Util.number import bytes_to_long, getPrime
from Crypto.Random import random
from sympy import sqrt_mod
from secret import FLAG
import os

FLAG += os.urandom(100)

def random_point(p,a,b):
    while True:
        x = random.randint(1, p-1)
        y2 = (pow(x, 3, p) + a*x + b) % p
        y = sqrt_mod(y2,p)
        if y != None:
            return x,y

def main():
    flag = bytes_to_long(FLAG)
    print("Welcome to my service!!! Choose the length of the prime, and we will provide something for you\n")
    while True:
        try:
            inp = int(input('Choose the bit length of the prime: '))
            assert inp > 1
            p = getPrime(inp)
            a,b = random.randint(1,p-1), random.randint(1,p-1)
            curve = ellipticcurve.CurveFp(p, a, b)
            x,y = random_point(p,a,b)
            P = ellipticcurve.Point(curve, x, y)
            Q = P*flag
            print(f"p = {p}")
            print(f"P = {P}")
            print(f"Q = {Q}")
        except Exception as e:
            print("Something wrong")
            
if __name__ == "__main__":
    main()