from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

p = 310717010502520989590157367261876774703
a = 2
b = 3

F = GF(p)
E = EllipticCurve(F, [a, b])

g_x = 179210853392303317793440285562762725654
g_y = 105268671499942631758568591033409611165
G = E.point((g_x, g_y))

P_x = 280810182131414898730378982766101210916
P_y = 291506490768054478159835604632710368904
P = E.point((P_x, P_y))

b_x = 272640099140026426377756188075937988094
b_y = 51062462309521034358726608268084433317
B = E.point((b_x, b_y))


primes = []
for f in factor(E.order()):
    primes.append(pow(f[0], f[1]))

dlogs = []
for prime in primes:
    t = E.order() // prime
    dlog = discrete_log(t * P, t * G, operation="+")
    dlogs.append(dlog)

n = CRT_list(dlogs, primes)

shared_secret = (B * n)[0]

sha1 = hashlib.sha1()
sha1.update(str(shared_secret).encode("ascii"))
key = sha1.digest()[:16]

iv = "07e2628b590095a5e332d397b8a59aa7"
enc_flag = "8220b7c47b36777a737f5ef9caa2814cf20c1c1ef496ec21a9b4833da24a008d0870d3ac3a6ad80065c138a2ed6136af"

cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv))
flag = cipher.decrypt(bytes.fromhex(enc_flag))
print(flag)
