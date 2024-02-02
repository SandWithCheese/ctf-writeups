from pwn import xor
from binascii import unhexlify

t1 = "0529242a631234122d2b36697f13272c207f2021283a6b0c7908"
t2 = "2f28202a302029142c653f3c7f2a2636273e3f2d653e25217908"
t3 = "322921780c3a235b3c2c3f207f372e21733a3a2b37263b313012"
t4 = "2f6c363b2b312b1e64651b6537222e37377f2020242b6b2c2d5d"
t5 = "283f652c2b31661426292b653a292c372a2f20212a316b283c09"
t6 = "29232178373c270f682c216532263b2d3632353c2c3c2a293504"
t7 = "613c37373531285b3c2a72273a67212a277f373a243c20203d5d"
t8 = "243a202a633d205b3c2d3765342236653a2c7423202f3f652a18"
t9 = "2239373d6f740a1e3c651f207f2c212a247f3d2e65262430791c"
t10 = "263e203d63232f0f20653f207f332065262c3168313722367918"
t11 = "2f2f372133202f142665212637222220733e383f2426386b"

print(t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8 + t9 + t10 + t11)

# t1 = unhexlify(t1)
# t2 = unhexlify(t2)
# t3 = unhexlify(t3)
# t4 = unhexlify(t4)
# t5 = unhexlify(t5)
# t6 = unhexlify(t6)
# t7 = unhexlify(t7)
# t8 = unhexlify(t8)
# t9 = unhexlify(t9)
# t10 = unhexlify(t10)
# t11 = unhexlify(t11)

# t1 = xor(t1, t2)
# t1 = xor(t1, t3)
# t1 = xor(t1, t4)
# t1 = xor(t1, t5)
# t1 = xor(t1, t6)
# t1 = xor(t1, t7)
# t1 = xor(t1, t8)
# t1 = xor(t1, t9)
# t1 = xor(t1, t10)
# t1 = xor(t1, t11)

# print(t1)
