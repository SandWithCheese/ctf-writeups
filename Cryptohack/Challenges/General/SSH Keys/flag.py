from Crypto.PublicKey import RSA

with open("bruce_rsa_6e7ecd53b443a97013397b1a1ea30e14.pub", "r") as f:
    key = RSA.importKey(f.read())

print(key.n)
