enc_flag = """                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                """

whitespace_char = " "

binary = ""
for char in enc_flag:
    if whitespace_char == char:
        binary += "1"
    else:
        binary += "0"

print(binary)
