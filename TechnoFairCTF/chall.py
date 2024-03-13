from sage.all import *
from Crypto.Util.number import *
import random
flag="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
flag=[ord(i) for i in flag]
flag=[flag[i:i+6] for i in range(0,len(flag),6)]

def gen_key():
	a=[random.getrandbits(16) for _ in range(6)]
	key=[[0]*_+[a[_]]+[0]*(5-_) for _ in range(6)]
	key=Matrix(key)
	return key

flag=Matrix(flag)
key = gen_key()
key=Matrix(key)

enc=flag*key
ev=key.eigenvectors_right()
enc=list(enc)

print(f"key_hint :{ev}")

print(f"enc : {enc}")


