#!/usr/bin/env python3
from Crypto.Util.number import *
import gmpy2

flag = "REDACTED"

e = 65537

p0 = getPrime(100)
q0 = getPrime(100)
p1 = getPrime(512)
p2 = gmpy2.next_prime(p1)
q1 = getPrime(512)
q2 = gmpy2.next_prime(q1)
p3 = getPrime(1024)
p4 = getPrime(1024)
p5 = getPrime(1024)
q3 = getPrime(1024)
q4 = getPrime(1024)
q5 = getPrime(1024)

n1 = p1*p2*q1*q2
n2 = p0*q0
n3 = p3*q3
n4 = p4*q4
n5 = p5*q5

c1 = pow(bytes_to_long(flag[0:len(flag)//2].encode('utf-8')),e,n1)
c1 = pow(c1,e,n1)
c1 = pow(c1,e,n1)
c2 = pow(bytes_to_long(flag[len(flag)//2:].encode('utf-8')),e,n2) # don't worry, the plaintext is not larger than n2
c2 = pow(c2,e,n1)
c3 = pow(c2,e//21845,n3)
c4 = pow(c2,e//21845,n4)
c5 = pow(c2,e//21845,n5)

print('c1 =', c1)
print('c3 =', c3)
print('c4 =', c4)
print('c5 =', c5)
print('n1 =', n1)
print('n2 =', n2)
print('n3 =', n3)
print('n4 =', n4)
print('n5 =', n5)
