#!/usr/bin/env python3

from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime, inverse, GCD
from random import sample, randint, shuffle

with open('spam.txt','r') as spam:
	spam = spam.read().splitlines()
	jumlah = randint(100, 200)
	email = sample(spam, jumlah)

with open('password.txt','r') as password:
	password = password.read().splitlines()
	full_password = ''.join(password)
	email.extend(password)
	shuffle(email)

with open('flag.txt','r') as flag:
	FLAG = flag.read().strip()

for idx in enumerate(email):
	indeks = idx[0]+1
	message = idx[1]
	while True:
		p = getPrime(512)
		q = getPrime(16)
		phi = (p-1)*(q-1)
		e = 65537
		d = inverse(e,phi)
		if GCD(e,phi) == 1 and d != -1:
			break

	m = bytes_to_long(message.encode())
	n = p*q
	c = pow(m,e,n)

	print(f'n{indeks} = {n}\n')
	print(f'c{indeks} = {c}\n')

answer = input('Input Full Password = ').strip()

if answer == full_password:
	print(f"Correct Password!\nHere's Your Flag\n{FLAG}\n")
else:
	print('Wrong Password!')
