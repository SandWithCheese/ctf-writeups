from Crypto.Util.number import getPrime, bytes_to_long

p = getPrime(512)
q = getPrime(512)
n = p * q

e = 88 # miles per hour required

flag = bytes_to_long(open("flag.txt", "rb").read())

c = pow(flag, e, n)

print(f"n = {n}")
print(f"p = {p}")
print(f"q = {q}")
print(f"e = {e}")
print(f"c = {c}")