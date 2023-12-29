import hashlib
import subprocess
from binascii import hexlify

wl_cmd = b"echo lol"
wl_hash = hashlib.sha1(wl_cmd).digest()[:3]



print(wl_hash)
