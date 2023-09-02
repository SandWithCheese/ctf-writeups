from Crypto.Cipher import AES

iv = b"hektoday" * 2
key = b"0000000010100100"
flag = "a06e6b249aea3f9fea49921babeed47dfc77d99da9577c126d9974a6db610f41fe6d6031eed99b3035e1d77dc1b2e3a9"
aes = AES.new(key, AES.MODE_CBC, iv=iv)
flag = aes.decrypt(flag)
print(flag)

# key = b"0000000101000101"
# aes = AES.new(key, AES.MODE_CBC, iv=iv)
# flag = aes.decrypt(flag)
