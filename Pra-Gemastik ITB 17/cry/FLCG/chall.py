from Crypto.Util.number import getPrime
from fractions import Fraction

# from flag import FLAG

FLAG = "CTFITB{REDACTED}"


from libnum import s2n


def prime(nbits=64):
    return getPrime(nbits)


base = prime()


def frac(nbits=64):
    a = Fraction(getPrime(nbits), base)
    if a > 1:
        a = 1 / a
    return a


class FLCG:
    def __init__(self):
        self.a = 2
        self.b = frac()
        self.m = prime(96) * prime(96)
        self.state = frac()

    def next_state(self):
        print(f"Numerator: {self.state.numerator}")
        print(f"Denominator: {self.state.denominator}")
        ret = self.state.numerator * pow(self.state.denominator, -1, self.m) % self.m
        self.state = (self.a * self.state) + self.b
        if self.state > 1:
            self.state = 1 / self.state
        print(f"State: {self.state}")
        return ret


c = FLCG()
o = open("test.txt", "w+")
o.write(str(c.m) + "\n")
exec(r"o.write(str(c.next_state())+'\n');" * 4)
exec(r"c.next_state();" * 50)
key = c.next_state()
pt = s2n(FLAG)
while key.bit_length() < pt.bit_length():
    key = pow(key, 2)

o.write(str(key ^ pt) + "\n")
