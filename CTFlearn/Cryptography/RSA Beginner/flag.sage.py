

# This file was *autogenerated* from the file flag.sage
from sage.all_cmdline import *   # import sage library

_sage_const_3 = Integer(3); _sage_const_219878849218803628752496734037301843801487889344508611639028 = Integer(219878849218803628752496734037301843801487889344508611639028); _sage_const_245841236512478852752909734912575581815967630033049838269083 = Integer(245841236512478852752909734912575581815967630033049838269083); _sage_const_0 = Integer(0); _sage_const_1 = Integer(1)
from Crypto.Util.number import long_to_bytes

e = _sage_const_3 
c = _sage_const_219878849218803628752496734037301843801487889344508611639028 
n = _sage_const_245841236512478852752909734912575581815967630033049838269083 

f = list(factor(n))
p = f[_sage_const_0 ][_sage_const_0 ]
q = f[_sage_const_1 ][_sage_const_0 ]

phi = (p - _sage_const_1 ) * (q - _sage_const_1 )
d = pow(e, -_sage_const_1 , phi)
m = pow(c, d, n)

print(long_to_bytes(m))
