#!/usr/bin/env python3

from sympy import nextprime
from Crypto.Util.number import *
from random import choice
from flag import flag
import sys


def get_pq(n):
	return getPrime(n), getPrime(n)

def get_token(l):
	return ''.join(choice('0123456789abcdef') for i in range(l))


correct = 0
while correct < 30:
	token = get_token(32)
	p, q = get_pq(256)
	ppq = p + q
	n = p * q
	e = 0x10001
	m = bytes_to_long(token.encode())
	c = pow(m,e,n)

	print(f'[*] {n = }')
	print(f'[*] {e = }')
	print(f'[*] {c = }')
	print(f'[*] {ppq = }')

	answer = input("[TOKEN]> ")
	if answer == token:
		correct += 1
		print()
	else:
		exit(0)

print(flag)