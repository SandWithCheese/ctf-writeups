from base64 import b64decode

binstr = "0011010100110011001000000011010100110011001000000011001100110010001000000011010100110010001000000011010100110011001000000011001100110010001000000011010100110010001000000011011000111001001000000011001100110010001000000011010100110011001000000011010100110011001000000011001100110010001000000011010100110011001000000011010100110000001000000011001100110010001000000011010100110100001000000011011000111001001000000011001100110010001000000011010100110101001000000011010100110010001000000011001100110010001000000011010100110001001000000011010100110001001000000011001100110010001000000011010100110010001000000011011000111000001000000011001100110010001000000011010100110010001000000011010100110110001000000011001100110010001000000011010100110100001000000011010100110010001000000011001100110010001000000011010100110100001000000011010100110100001000000011001100110010001000000011010100110100001000000011010100110001001000000011001100110010001000000011010100110101001000000011011000110101001000000011001100110010001000000011010100110010001000000011010100110000001000000011001100110010001000000011010100110100001000000011010100110100001000000011001100110010001000000011010100110100001000000011010100110000001000000011001100110010001000000011010100110011001000000011010100110010001000000011001100110010001000000011010100110011001000000011010100110000001000000011001100110010001000000011010100110101001000000011010100110011001000000011001100110010001000000011010100110100001000000011010100110011001000000011001100110010001000000011010100110011001000000011010100110100001000000011001100110010001000000011010100110001001000000011010100110111001000000011001100110010001000000011010100110101001000000011010100110011001000000011001100110010001000000011010100110100001000000011010100110010001000000011001100110010001000000011010100110011001000000011010100110101001000000011001100110010001000000011010100110001001000000011010000111001001000000011001100110010001000000011010100110100001000000011010100110111001000000011001100110010001000000011010100110011001000000011011000110101001000000011001100110010001000000011010100110011001000000011010100110110001000000011001100110010001000000011010100110010001000000011010100110111001000000011001100110010001000000011010100110001001000000011010000111001001000000011001100110010001000000011010100110100001000000011010100110100001000000011001100110010001000000011010100110011001000000011010000111001001000000011001100110010001000000011010100110001001000000011011000111000001000000011001100110010001000000011010100110001001000000011011000111000"

decoded = ""
for i in range(0, len(binstr), 8):
    block = binstr[i : i + 8]
    decoded += chr(int(block, 2))

decoded = decoded.split()

decoded_2 = ""
for i in decoded:
    decoded_2 += chr(int(i))

decoded_2 = decoded_2.split()
flag = ""
for i in decoded_2:
    flag += chr(int(i, 16))

print(b64decode(flag).decode())