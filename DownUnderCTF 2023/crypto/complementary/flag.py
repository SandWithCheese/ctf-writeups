from factordb.factordb import FactorDB
from Crypto.Util.number import long_to_bytes

n = 6954494065942554678316751997792528753841173212407363342283423753536991947310058248515278

f = FactorDB(n)
f.connect()
factors = f.get_factor_list()

p = 1
for i in range(len(factors) - 1):
    p *= factors[i]

flag = long_to_bytes(p) + long_to_bytes(factors[-1])
print(flag.decode())
