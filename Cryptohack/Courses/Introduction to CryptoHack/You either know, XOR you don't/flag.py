from binascii import unhexlify
from Crypto.Util.number import bytes_to_long, long_to_bytes

flag = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"

# decrypt = bytes_to_long(unhexlify(flag)[:7])
decrypt = bytes_to_long(unhexlify(flag))
# print(len(decrypt))


# key = bytes_to_long(b"crypto{")
key = bytes_to_long(b"myXORkeymyXORkeymyXORkeymyXORkeymyXORkeymy")
# decoded = "".join(chr(b ^ key) for b in decrypt)
print(long_to_bytes(decrypt ^ key))
