from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from random import randint
# from secret import flag, noncetoken
flag = b"IFEST{REDACTED}"
noncetoken = 0xdeadbeef

class Cipher:
    def __init__(self, g=5, p=None):
        if p == None:
            self.p = getPrime(400)
        else:
            self.p = p

        self.g = g
        self.x = randint(1, self.p-2)
        self.h = pow(g, self.x, self.p)
        self.y = randint(1, self.p-1)
        self.counter = 0

    def get_pubkey(self):
        return self.g, self.p, self.h

    def get_privkey(self):
        return self.x

    def shift_nonce(self):
        self.counter += 1
        return self.y >> (10 * ((noncetoken >> self.counter) & 1))

    def encrypt(self, m):
        y = self.shift_nonce()
        s = pow(self.h, y, self.p)
        print(f"S from encrypt {m}: {s}")
        c1 = int(str(self.counter) + str(pow(self.g, y + self.counter, self.p)))
        c2 = m * (s + self.counter) % self.p 
        return c1, c2

    def decrypt(self, c1, c2, x=None):
        if x == None: x = self.x
        curr_count = int(str(c1)[:1])
        c1 = int(str(c1)[1:]) * pow(self.g ** curr_count, -1, self.p)
        s = pow(c1, x, self.p)
        print(f"S from decrypt: {s}")
        return c2 * pow(s + curr_count, -1, p) % p

cipher = Cipher()
g, p, h = cipher.get_pubkey()
print(f"g = {g}")
print(f"p = {p}")
print(f"h = {h}")

header = b"<=== ELG === Message to Alice === ELG ===>"
m = bytes_to_long(flag)
print(f"Head: {cipher.encrypt(bytes_to_long(header))}")
print(f"Body: {cipher.encrypt(m)}")
# print(f"Decrypt with this: {cipher.get_privkey()}")

body = cipher.encrypt(m)

print(f"Decrypt: {long_to_bytes(cipher.decrypt(body[0], body[1]))}")