from Crypto.Util.number import inverse
from fractions import Fraction

m = 3008875652368211596244815471350462038792232085258709227391
a = 2
x1 = 1826098110371268016684002331858214550300384545361833355863
x2 = 347245037727060974037376263170237758431123061431679380950
x3 = 2876728541302860516100551854656038500731603653881233226827
x4 = 1611093742370573118248956020923085251631733337677037535305
enc = 41233880896321254459866349268884511942725574774461045364214954954210330057734619491369710247463540998176466098331326646742321996551513849100829647364314540578323545719439713844015023853719039306920300825972619422763106382356016620

# b = p/q
# state = r/s

# x1 = r0 * inv(s0, m) mod m
# x2 = r1 * inv(s1, m) mod m
# x3 = r2 * inv(s2, m) mod m
# x4 = r3 * inv(s3, m) mod m

# Next state is either
# (2r + ps) / qs
# or
# qs / 2r + ps

# # x2 = a*x1 + c mod p
# # x2 - a*x1 = c mod p
# c = (x2 - a * x1) % p

# print(c)

# # x1 = a*x0 + c mod p
# # x1 - c = a*x0 mod p
# x0 = (x1 - c) * inverse(a, p) % p

# print(x0)


# class FLCG:
#     def __init__(self):
#         self.a = 2
#         self.b = c
#         self.m = p
#         self.state = Fraction(p, x0)

#     def next_state(self):
#         ret = self.state.numerator * pow(self.state.denominator, -1, self.m) % self.m
#         self.state = (self.a * self.state) + self.b
#         if self.state > 1:
#             self.state = 1 / self.state
#         return ret


# lcg = FLCG()

# for i in range(5):
#     print(lcg.state)
#     lcg.next_state()
