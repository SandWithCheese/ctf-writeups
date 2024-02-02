from Crypto.Util.number import long_to_bytes

e = 3
c = 219878849218803628752496734037301843801487889344508611639028
n = 245841236512478852752909734912575581815967630033049838269083

f = list(factor(n))
p = f[0][0]
q = f[1][0]

phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
m = pow(c, d, n)

print(long_to_bytes(m))
