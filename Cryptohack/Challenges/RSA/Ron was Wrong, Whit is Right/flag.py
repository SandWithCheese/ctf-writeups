from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from sympy import gcd

arr_of_n = []
for i in range(1, 51):
    with open(f"./keys_and_messages/{i}.pem") as f:
        key = RSA.importKey(f.read())
        arr_of_n.append(key.n)

with open("./keys_and_messages/21.pem") as f:
    key = RSA.importKey(f.read())
    n = key.n

for i in range(len(arr_of_n)):
    if i == 20:
        continue
    cd = gcd(n, arr_of_n[i])
    if cd != 1:
        p = n // cd
        q = cd

        phi = int((p - 1) * (q - 1))
        e = key.e
        d = pow(e, -1, phi)
        key = RSA.construct((n, e, d, int(p), int(q)))
        cipher = PKCS1_OAEP.new(key)
        with open(f"./keys_and_messages/21.ciphertext", "r") as f:
            ciphertext = f.read()
        print(cipher.decrypt(bytes.fromhex(ciphertext)).decode())
