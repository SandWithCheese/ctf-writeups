from pwn import xor

enc = b"\t\x1b\x11\x00\x16\x0b\x1d\x19\x17\x0b\x05\x1d(\x05\x005\x1b\x1f\t,\r\x00\x18\x1c\x0e"
key = b"jowls"

print(xor(enc, key))
