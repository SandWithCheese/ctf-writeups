from itertools import cycle

key = b"AMD64b701"  # example – use the real one you recover
data = open("background.png", "rb").read()[-1536 - 16 : -16]
# print(data)
out = bytes(d ^ k for d, k in zip(data, cycle(key)))
open("extra_dec.bin", "wb").write(out)
