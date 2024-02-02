from Crypto.Util.number import long_to_bytes, bytes_to_long, getPrime
from pwn import xor
import random
from sympy.ntheory import isprime

q = 81950208731605030173072901497240676460946134422613059941413476068465656250011
c = 1913607487336850198612381177842742944535528551492332730687709803333994170933334235248158693072452023061642877943692858799822420964044267542215434514413393
e = 65537

# seed = bytes_to_long(xor(b"usedistofindouttheseed", b"thisisthekeytogetyourseed"))
# seed = bytes_to_long(b"usedistofindouttheseed") ^ bytes_to_long(
#     b"thisisthekeytogetyourseed",
# )

# print(seed == aseed)

# random.seed(seed)

# p = random.getrandbits(256)
# while not isprime(p):
#     p = random.getrandbits(256)

# n = p * q
# phi = (p - 1) * (q - 1)
# d = pow(e, -1, phi)

# m = pow(c, d, n)
# print(long_to_bytes(m))
