def decrypt(plaintext, key):
    cipher = []
    for char in plaintext:
        cipher.append(chr(char // (key * 311)))
    return cipher


def dynamic_xor_decrypt(ciphertext, text_key):
    plaintext = ""
    key_length = len(text_key)
    for i, char in enumerate(ciphertext):
        key_char = text_key[i % key_length]
        decrypted_char = chr(ord(char) ^ ord(key_char))
        plaintext += decrypted_char
    return plaintext


cipher = [
    151146,
    1158786,
    1276344,
    1360314,
    1427490,
    1377108,
    1074816,
    1074816,
    386262,
    705348,
    0,
    1393902,
    352674,
    83970,
    1141992,
    0,
    369468,
    1444284,
    16794,
    1041228,
    403056,
    453438,
    100764,
    100764,
    285498,
    100764,
    436644,
    856494,
    537408,
    822906,
    436644,
    117558,
    201528,
    285498,
]

decipher = decrypt(cipher, 54)
semi_decipher = dynamic_xor_decrypt(decipher, "trudeau")

print(semi_decipher[::-1])
