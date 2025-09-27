import binascii
import zlib

# Load the decrypted flag file
with open("flag.enc.i", "rb") as f:
    data = f.read()

# Skip the 12-byte revlog header
payload = data[12:]

# Some revlog payloads are zlib-compressed, try decompressing
try:
    flag = zlib.decompress(payload)
    print("Recovered flag:", flag.decode())
except zlib.error:
    # If not compressed, just decode as ASCII
    flag = "".join([chr(b) if 32 <= b < 127 else "." for b in payload])
    print("Recovered flag:", flag)
