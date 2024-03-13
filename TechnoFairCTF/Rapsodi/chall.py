import random
from Crypto.Util.number import *

flag="XXXXXXXXXXXXXXXXXXXXXXXXX"

class lcg:
	def __init__(self,a,b,n):
		self.seed=random.getrandbits(32)
		self.a=(a-(a&1))
		self.b=b
		self.n=(n-(n&1))
	def next(self):
		self.seed=(self.a*self.seed+self.b)%self.n
		return self.seed

a1,a2,b1,b2,n1,n2=[random.getrandbits(32) for _ in range(6)]

if((b1^b2)&1==0):
	b1-=1



lcg1=lcg(a1,b1,n1)
lcg2=lcg(a2,b2,n2)

s1=lcg1.next()
s2=lcg2.next()
enc=[]

flag=''.join(['{:08b}'.format(ord(i)) for i in flag])
for i in flag:
	if i=='0':
		enc.append(s1)	
		s1=lcg1.next()
	else:
		enc.append(s2)
		s2=lcg2.next()

print(f"enc: {enc}")