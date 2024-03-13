from Crypto.Util.number import long_to_bytes
from factordb.factordb import FactorDB
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

n = int(
    "4ca21ede37e3d6a63bcee5f9120d0989f0143aae915302f346e8abbb840a72fb56d1487528ca75195b7832628389092c4e893fa4a6c9b0114266e805b12dc08d",
    16,
)
e = 0x10001
c = int(
    "249d72cd1d287b1a15a3881f2bff5788bc4bf62c789f2df44d88aae805b54c9a94b8944c0ba798f70062b66160fee312b98879f1dd5d17b33095feb3c5830d28",
    16,
)

f = FactorDB(n)
f.connect()

p, q = f.get_factor_list()

phi = (p - 1) * (q - 1)

d = pow(e, -1, phi)
# pl = pow(c, d, n)

# print(long_to_bytes(pl))

key = RSA.construct((n, e, d))
cipher = PKCS1_OAEP.new(key)
plaintext = cipher.decrypt(bytes.fromhex(hex(c)[2:]))
print(plaintext.decode())
