charset = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
encoded_flag = (
    '*&(&)<+$*"$%+?_?:.,[;[+~+{](+`#%,|![{[*;.]^@}@,>\'.:@)_"<+.:?+`>$\'"#$#`=((|};'
)

binstr = ""
for char in encoded_flag:
    idx = charset.index(char)
    binstr += format(idx, "05b")

binstr = binstr[:-4]

for i in range(0, len(binstr), 8):
    block = binstr[i : i + 8]
    print(chr(int(block, 2)), end="")
