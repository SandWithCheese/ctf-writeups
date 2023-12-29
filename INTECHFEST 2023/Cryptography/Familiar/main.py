def encode(data):
    charset = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    padd = "="

    binstr = "".join(format(byte, "08b") for byte in data)
    padding = (5 - len(binstr) % 5) % 5
    binstr += "0" * padding
    groups = [binstr[i:i+5] for i in range(0, len(binstr), 5)]

    result = ""
    for group in groups:
        dec = int(group, 2)
        result += charset[dec]

    result += padd * (padding // 2)
    return result

FLAG = "flag{fake_flag_dont_submit}"
print(encode(FLAG.encode()))