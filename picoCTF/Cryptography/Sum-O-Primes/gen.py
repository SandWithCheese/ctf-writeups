#!/usr/bin/python

from binascii import hexlify
from gmpy2 import mpz_urandomb, next_prime, random_state
import math
import os
import sys

if sys.version_info < (3, 9):
    import gmpy2

    math.gcd = gmpy2.gcd
    math.lcm = gmpy2.lcm

FLAG = open("flag.txt").read().strip()
FLAG = int(hexlify(FLAG.encode()), 16)
SEED = int(hexlify(os.urandom(32)).decode(), 16)
STATE = random_state(SEED)


def get_prime(bits):
    return next_prime(mpz_urandomb(STATE, bits) | (1 << (bits - 1)))


p = get_prime(1024)
q = get_prime(1024)

x = p + q
n = p * q

e = 65537

m = math.lcm(p - 1, q - 1)
d = pow(e, -1, m)

c = pow(FLAG, e, n)

print(f"x = {x:x}")
print(f"n = {n:x}")
print(f"c = {c:x}")

# x = 237794038489937295292404845103332168586899775764009768813015783887873829658685908155889292284052042307072192057431831496692141879605590713811965921260098180449961810125614556736808532544155958113715066723941821777772381016342333402246835346563333191665490232676273977656868220862198101771730081310274761841070
# n = 14107968002788601163232271919683185628377930258855714024361251700443482916159477972019175057249307805020558833578002642814353244251935462643122106832841875886751834868578847553067993029534859873400111872030760141512265217100084094768240561746973517000260205166788073707007901559501857058570047904411103289205303895005723927634856272992046301957255183083869294681094092965797803167854696071500371486827898745037887826839037430790364261755123274123835361705705618196178336329858713462923973567226715396383555224515182961278023099436837662748725809380387313268345922304316857780150905037767522499166165808213903858699409
# c = 2862537339040469147429657894344199928557031834390107583219729603518151458232752655435765178741847862681985518014369908230465656681188452816388220057841477741951807370846472046013718654924186479831297315008200827303965506316115312185032136602875438400387736740902196374239905780326853099910635897462206320968355042526152404835351422548524752308082386282793614300087991456840160462341088790668081742054292524665828459909511307682427456625705560299547231552417332610842874439163798240180613567066151575717456490027272337259628798278336279800627826934011806508731399100283618512809664315701708126217489999299504239618063