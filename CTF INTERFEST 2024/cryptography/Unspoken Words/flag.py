with open("encoded.txt") as f:
    enc = f.read().strip()

morse = ""
for i in enc:
    if i == "🥺":
        morse += "-"
    elif i == "😍":
        morse += "."
    else:
        morse += "/"

print(morse)
