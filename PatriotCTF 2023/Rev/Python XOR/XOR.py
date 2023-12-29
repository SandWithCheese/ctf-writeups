from string import punctuation

alphabet = list(punctuation)
data = "bHEC_T]PLKJ{MW{AdW]Y"


def main():
    #   For loop goes here
    for i in alphabet:
        key = i
        decrypted = "".join([chr(ord(x) ^ ord(key)) for x in data])
        if "Flag" in decrypted:
            print(decrypted)
            break


main()
