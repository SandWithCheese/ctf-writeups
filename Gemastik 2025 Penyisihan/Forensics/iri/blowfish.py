from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import unpad
import binascii

# Replace with your actual key and IV
key = b"SuperSecretKey!!"
iv = b"12345678"
BLOCK_SIZE = Blowfish.block_size  # 8

# Hex content of your .i file (without spaces/newlines)
with open("./stage/flag.enc", "rb") as f:
    hex_data = f.read()
    hex_data = hex_data.hex()
    print(hex_data)

# Convert hex to bytes
ciphertext = binascii.unhexlify(hex_data)

cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
decrypted_data = cipher.decrypt(ciphertext)

# Unpad plaintext
try:
    plaintext = unpad(decrypted_data, BLOCK_SIZE)
except ValueError:
    plaintext = decrypted_data  # if padding is non-standard

# Print the recovered flag
print("Recovered flag:", plaintext.decode(errors="ignore"))

with open("flag.enc", "wb") as f:
    f.write(plaintext)
