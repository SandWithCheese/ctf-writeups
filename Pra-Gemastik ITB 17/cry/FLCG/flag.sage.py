

# This file was *autogenerated* from the file flag.sage
from sage.all_cmdline import *   # import sage library

_sage_const_4 = Integer(4); _sage_const_3 = Integer(3); _sage_const_1 = Integer(1); _sage_const_2 = Integer(2); _sage_const_0 = Integer(0); _sage_const_3008875652368211596244815471350462038792232085258709227391 = Integer(3008875652368211596244815471350462038792232085258709227391); _sage_const_1826098110371268016684002331858214550300384545361833355863 = Integer(1826098110371268016684002331858214550300384545361833355863); _sage_const_347245037727060974037376263170237758431123061431679380950 = Integer(347245037727060974037376263170237758431123061431679380950); _sage_const_2876728541302860516100551854656038500731603653881233226827 = Integer(2876728541302860516100551854656038500731603653881233226827); _sage_const_1611093742370573118248956020923085251631733337677037535305 = Integer(1611093742370573118248956020923085251631733337677037535305); _sage_const_41233880896321254459866349268884511942725574774461045364214954954210330057734619491369710247463540998176466098331326646742321996551513849100829647364314540578323545719439713844015023853719039306920300825972619422763106382356016620 = Integer(41233880896321254459866349268884511942725574774461045364214954954210330057734619491369710247463540998176466098331326646742321996551513849100829647364314540578323545719439713844015023853719039306920300825972619422763106382356016620)
from math import gcd


def attack(y, m=None, a=None, c=None):
    """
    Recovers the parameters from a linear congruential generator.
    If no modulus is provided, attempts to recover the modulus from the outputs (may require many outputs).
    If no multiplier is provided, attempts to recover the multiplier from the outputs (requires at least 3 outputs).
    If no increment is provided, attempts to recover the increment from the outputs (requires at least 2 outputs).
    :param y: the sequential output values obtained from the LCG
    :param m: the modulus of the LCG (can be None)
    :param a: the multiplier of the LCG (can be None)
    :param c: the increment of the LCG (can be None)
    :return: a tuple containing the modulus, multiplier, and the increment
    """
    if m is None:
        assert len(y) >= _sage_const_4 , "At least 4 outputs are required to recover the modulus"
        for i in range(len(y) - _sage_const_3 ):
            d0 = y[i + _sage_const_1 ] - y[i]
            d1 = y[i + _sage_const_2 ] - y[i + _sage_const_1 ]
            d2 = y[i + _sage_const_3 ] - y[i + _sage_const_2 ]
            g = d2 * d0 - d1 * d1
            m = g if m is None else gcd(g, m)

        assert is_prime_power(
            m
        ), "Modulus must be a prime power, try providing more outputs"

    gf = GF(m)
    if a is None:
        assert len(y) >= _sage_const_3 , "At least 3 outputs are required to recover the multiplier"
        x0 = gf(y[_sage_const_0 ])
        x1 = gf(y[_sage_const_1 ])
        x2 = gf(y[_sage_const_2 ])
        a = int((x2 - x1) / (x1 - x0))

    if c is None:
        assert len(y) >= _sage_const_2 , "At least 2 outputs are required to recover the multiplier"
        x0 = gf(y[_sage_const_0 ])
        x1 = gf(y[_sage_const_1 ])
        c = int(x1 - a * x0)

    return m, a, c


p = _sage_const_3008875652368211596244815471350462038792232085258709227391 
a = _sage_const_2 
x1 = _sage_const_1826098110371268016684002331858214550300384545361833355863 
x2 = _sage_const_347245037727060974037376263170237758431123061431679380950 
x3 = _sage_const_2876728541302860516100551854656038500731603653881233226827 
x4 = _sage_const_1611093742370573118248956020923085251631733337677037535305 
enc = _sage_const_41233880896321254459866349268884511942725574774461045364214954954210330057734619491369710247463540998176466098331326646742321996551513849100829647364314540578323545719439713844015023853719039306920300825972619422763106382356016620 

m, a, c = attack([x1, x2, x3, x4], m=p, a=a)

print(m, a, c)
