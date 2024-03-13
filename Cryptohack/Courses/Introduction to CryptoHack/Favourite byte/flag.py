from binascii import unhexlify
from Crypto.Util.number import bytes_to_long, long_to_bytes

flag = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"

decrypt = unhexlify(flag)
# for key in range(256):
#     decoded = "".join(chr(b ^ key) for b in decrypt)

#     print(key, decoded)

key = 16
decoded = "".join(chr(b ^ key) for b in decrypt)
print(decoded)
