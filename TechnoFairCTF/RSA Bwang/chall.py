import hashlib
import os
from secret import flag
import binascii
from Crypto.Util.number import *
from sympy import *

def gen():
	p=getStrongPrime(1024)
	q=getStrongPrime(1024)
	r=getStrongPrime(1024)
	return p,q,r



m1,m2=flag[:len(flag)//2],flag[len(flag)//2:]
m1=bytes_to_long(m1)
m2=bytes_to_long(m2)

p1,q1,p2=gen()
q2=q1
n1=p1*q1
n2=p2*q2
e1=0x10001
e2=0x10001

ct1=pow(m1,e1,n1)
ct2=pow(m2*(n2-1),e2,n2)

p1tambahq1=p1+q1

print(f"n1  = {n1}")
print(f"e1  = {e1}")
print(f"ct1 = {ct1}")
print(f"p1tambahq1 = {p1+q1}")

print(f"n2  = {n2}")
print(f"e2  = {e2}")
print(f"ct2 = {ct2}")


