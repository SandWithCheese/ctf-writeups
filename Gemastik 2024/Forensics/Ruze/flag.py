from Crypto.Cipher import AES

with open("seccreettttt_credentialll_confidentalll_moodd_booossteerrrr.pdf", "rb") as f:
    enc = f.read()[16:]

IV = b"15ccfc351be2d69c"
KEY = b"ea0aaa5d53dddfe1"

aes = AES.new(KEY, AES.MODE_CBC, IV)

dec = aes.decrypt(enc)

with open("flag.pdf", "wb") as f:
    f.write(dec)
