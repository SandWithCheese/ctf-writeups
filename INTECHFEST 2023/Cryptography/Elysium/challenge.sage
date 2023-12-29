from Crypto.Util.number import bytes_to_long
from sage.all import *


def add(G, P):
    return 288*G + 21*P


flag = open('flag.txt', 'rb').read()

p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
K = GF(p)
a = 115792089210356248762697446949407573530086143415290314195533631308867097853948
b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
E = EllipticCurve(K, (a, b))

G = E.gens()[0]

m = bytes_to_long(flag)
P = E.lift_x(Integer(m))
Q = add(G, P)

print('Q:', Q)
