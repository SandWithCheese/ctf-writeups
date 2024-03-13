from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib


def is_pkcs7_padded(message):
    padding = message[-message[-1] :]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode("ascii"))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode("ascii")
    else:
        return plaintext.decode("ascii")


shared_secret = 6845992834990977198
iv = "f7c0ef4a1403d4dd064c55f4532b9ad3"
ciphertext = "c6c5b6fa8911267cc7d78f16133974c73dc5f75cdf87744b97c7f43ed6890c67"

# A = g^a mod p
# B = g^a mod p
# s = B^a mod p = A^b mod p

print(decrypt_flag(shared_secret, iv, ciphertext))
