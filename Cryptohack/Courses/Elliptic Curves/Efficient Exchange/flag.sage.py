

# This file was *autogenerated* from the file Efficient Exchange/flag.sage
from sage.all_cmdline import *   # import sage library

_sage_const_9739 = Integer(9739); _sage_const_497 = Integer(497); _sage_const_1768 = Integer(1768); _sage_const_4726 = Integer(4726); _sage_const_6534 = Integer(6534); _sage_const_3 = Integer(3); _sage_const_2 = Integer(2); _sage_const_0 = Integer(0)
F = GF(_sage_const_9739 , names=('x',)); (x,) = F._first_ngens(1)
E = EllipticCurve(F, [_sage_const_497 , _sage_const_1768 ])

q_x = _sage_const_4726 
nB = _sage_const_6534 

y_2 = (pow(q_x, _sage_const_3 , _sage_const_9739 ) + _sage_const_497  * q_x + _sage_const_1768 ) % _sage_const_9739 
f = x**_sage_const_2  - y_2

ys = [i[_sage_const_0 ] for i in f.roots()]

# F = Zmod(9739)
# E = EllipticCurve(F, [497, 1768])

for y in ys:
    Q = E([q_x, y])

    S = nB * Q
    print(f"Found: {S[_sage_const_0 ]}")
    break
