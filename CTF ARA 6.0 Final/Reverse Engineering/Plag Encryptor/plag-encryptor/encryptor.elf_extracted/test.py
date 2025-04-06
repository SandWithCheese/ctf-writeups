with open("plag.txt", "wb") as f:
    f.write(b"\x00" * 16)

with open("plag.txt.enc", "rb") as f:
    enc = f.read()

pt = b"\x00" * 16
ct = enc[:16]
key = enc[16:24]
iv = enc[24:]

from Crypto.Cipher import AES

cipher = AES.new(key, AES.MODE_OCB)
pt = cipher.decrypt(ct)
print(pt)
