

# This file was *autogenerated* from the file flag.sage
from sage.all_cmdline import *   # import sage library

_sage_const_5 = Integer(5); _sage_const_1731712993620621198627916942825579093696110648615008640172315786615453905886335641266637036327082384969765802941354527473 = Integer(1731712993620621198627916942825579093696110648615008640172315786615453905886335641266637036327082384969765802941354527473); _sage_const_1714959585068483700163613820136766390436247182557995830728451023386355964649869435087668382332656176806274880455667538560 = Integer(1714959585068483700163613820136766390436247182557995830728451023386355964649869435087668382332656176806274880455667538560); _sage_const_155624726976950326527498625554762366503090432785998836658282421203213996889991034300935039975238809168968527486068834991 = Integer(155624726976950326527498625554762366503090432785998836658282421203213996889991034300935039975238809168968527486068834991); _sage_const_1434911128320227865388406395322220300576084099875900575337993125089881668459239455527441213719682636083337524734625076873 = Integer(1434911128320227865388406395322220300576084099875900575337993125089881668459239455527441213719682636083337524734625076873); _sage_const_2168311167517714515383383238799989487213548508021200163484960894185447265062131318543675864045082245663495252901622081209 = Integer(2168311167517714515383383238799989487213548508021200163484960894185447265062131318543675864045082245663495252901622081209); _sage_const_1160502936782935692476508416409681722376638504002330705634995790656410154608499395611346394295925367148309335396583879114 = Integer(1160502936782935692476508416409681722376638504002330705634995790656410154608499395611346394295925367148309335396583879114); _sage_const_1 = Integer(1); _sage_const_2 = Integer(2)
from Crypto.Util.number import bytes_to_long, long_to_bytes

g = _sage_const_5 
p = _sage_const_1731712993620621198627916942825579093696110648615008640172315786615453905886335641266637036327082384969765802941354527473 
h = _sage_const_1714959585068483700163613820136766390436247182557995830728451023386355964649869435087668382332656176806274880455667538560 
Head = (
    _sage_const_155624726976950326527498625554762366503090432785998836658282421203213996889991034300935039975238809168968527486068834991 ,
    _sage_const_1434911128320227865388406395322220300576084099875900575337993125089881668459239455527441213719682636083337524734625076873 ,
)
Body = (
    _sage_const_2168311167517714515383383238799989487213548508021200163484960894185447265062131318543675864045082245663495252901622081209 ,
    _sage_const_1160502936782935692476508416409681722376638504002330705634995790656410154608499395611346394295925367148309335396583879114 ,
)


header = b"<=== ELG === Message to Alice === ELG ===>"
m_header = bytes_to_long(header)
inv_m_header = pow(m_header, -_sage_const_1 , p)

c2 = Head[_sage_const_1 ]
s = (c2 * inv_m_header % p) - _sage_const_1 
print(f"s: {s}")

print(m_header * (s + _sage_const_1 ) % p)


c2 = Body[_sage_const_1 ]

inv_s = pow(s + _sage_const_2 , -_sage_const_1 , p)
flag = (c2 * inv_s) % p

# c2 = m * (s + self.counter) % self.p

# flag = (c2 * pow(s + 2, -1, p)) % p

print(long_to_bytes(flag))
