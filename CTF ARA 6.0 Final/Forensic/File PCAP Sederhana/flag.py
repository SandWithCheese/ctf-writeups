from Crypto.Cipher import AES
import hashlib, base64
# Import pad
from Crypto.Util.Padding import pad

ciphertext = base64.b64decode("3D22URHPkA0BYR43/Jo6BQ==")
key = hashlib.md5(b"https://www.bing.com/").digest()
iv = b"23052700"  # Replace with correct dHis from when it was encrypted

cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(ciphertext)

print(plaintext)
