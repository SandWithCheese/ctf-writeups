import subprocess
from string import printable

keys = [
    "ae",
    "an",
    "ar",
    "as",
    "be",
    "bl",
    "bo",
    "bu",
    "ca",
    "ce",
    "ch",
    "co",
    "da",
    "de",
    "di",
    "do",
    "ed",
    "en",
    "er",
    "es",
    "ha",
    "he",
    "hi",
    "ho",
    "im",
    "in",
    "is",
    "it",
    "le",
    "li",
    "ll",
    "ly",
    "ma",
    "me",
    "mi",
    "mo",
    "nd",
    "ne",
    "ng",
    "nt",
    "of",
    "on",
    "or",
    "ou",
    "ra",
    "re",
    "ri",
    "ro",
    "se",
    "sh",
    "si",
    "st",
    "te",
    "th",
    "ti",
    "to",
    "ul",
    "ur",
    "us",
    "ut",
    "wa",
    "we",
    "wh",
    "wi",
]

# payload = "netcomp{ev"
payload = "netcomp{even_when_you_had_two_eyes_you_d_see_only_half_the_pict"
print(payload)
with open("flag.netcomp", "rb") as f:
    flag = f.read()
    print(flag)

while payload[-1] != "}":
    for key in keys:
        temp = payload + key
        with open("test.txt", "w") as f:
            f.write(temp)

        subprocess.run(["./netcompressor", "test.txt"])

        with open("test.netcomp", "rb") as f:
            brute = f.read()

        if flag.startswith(brute):
            payload += key
            print(brute)
            print(payload)
            break
    else:
        for char in printable:
            temp = payload + char
            with open("test.txt", "w") as f:
                f.write(temp)

            subprocess.run(["./netcompressor", "test.txt"])

            with open("test.netcomp", "rb") as f:
                brute = f.read()

            if flag.startswith(brute):
                payload += char
                print(brute)
                print(payload)
                break
        else:
            print(brute)
            print("Not found")
            break
