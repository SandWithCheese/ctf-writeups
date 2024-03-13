import string

LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]


def b16_encode(plain):
    enc = ""
    for c in plain:
        binary = "{0:08b}".format(ord(c))
        enc += ALPHABET[int(binary[:4], 2)]
        enc += ALPHABET[int(binary[4:], 2)]
    return enc


def b16_decode(enc):
    plain = ""
    for i in range(0, len(enc), 2):
        binary = "{0:04b}{1:04b}".format(
            ALPHABET.index(enc[i]), ALPHABET.index(enc[i + 1])
        )
        plain += chr(int(binary, 2))
    return plain


def shift(c, k):
    t1 = ord(c) - LOWERCASE_OFFSET
    t2 = ord(k) - LOWERCASE_OFFSET
    return ALPHABET[(t1 + t2) % len(ALPHABET)]


def unshift(i, k):
    t2 = ord(k) - LOWERCASE_OFFSET
    if i > t2:
        t1 = i - t2
    else:
        t1 = i + 16 - t2 - 1

    return chr(t1 + LOWERCASE_OFFSET)


# flag = "redacted"
# key = "redacted"
# assert all([k in ALPHABET for k in key])
# assert len(key) == 1

# b16 = b16_encode(flag)
# enc = ""
# for i, c in enumerate(b16):
#     enc += shift(c, key[i % len(key)])

flag = "mlnklfnknljflfmhjimkmhjhmljhjomhmmjkjpmmjmjkjpjojgjmjpjojojnjojmmkmlmijimhjmmj"
# for char in flag:
#     print(ALPHABET.index(char), end=" ")

for key in ALPHABET:
    decoded = ""
    for char in flag:
        decoded += unshift(ALPHABET.index(char), key)
    print(b16_decode(decoded))

b16 = []

for i in range(len(ALPHABET)):
    b16.append("")

for i in flag:
    for k in range(len(ALPHABET)):
        index = ALPHABET.index(i)
        if k <= index:
            b16[k] += chr(index - k + 97)
        else:
            b16[k] += chr(index + 16 - k + 97)

for k in range(len(ALPHABET)):
    flag = ""
    b = b16[k]
    for i in range(0, len(b), 2):
        if b[i + 1] in ALPHABET and b[i] in ALPHABET:
            index1 = ALPHABET.index(b[i])
            index2 = ALPHABET.index(b[i + 1])
            flag += chr((index1 << 4) + index2)
    print(flag)
