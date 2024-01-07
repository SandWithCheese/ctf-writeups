from Crypto.Util.number import long_to_bytes

p = 1089915817272225657529571741047
q = 1230438593754451648545439211911
e = 65537

cp = 432129069781466954970115267255448126809679346680737712720914

n = p * q
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
m = pow(cp, d, n)

print(long_to_bytes(m).decode())
