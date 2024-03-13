ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

with open("message.txt", "r") as f:
    arr = f.readlines()
    key = arr[0][:-1].strip()
    decode = arr[1:]
    flag = decode[-1]
    for text in decode:
        if text == "\n":
            continue
        if flag == text:
            for character in text:
                upper = character.upper()
                if upper not in ALPHABET:
                    print(character, end="")
                    continue
                print(ALPHABET[key.index(upper)], end="")
            print()
            break

        text = text[:-1]
        for character in text:
            if character in [" ", ",", ".", "—"]:
                print(character, end="")
                continue
            print(ALPHABET[key.index(character.upper())], end="")
        print()
