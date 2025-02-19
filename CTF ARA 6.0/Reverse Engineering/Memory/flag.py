def generate_flag():
    content = []
    for i in range(5):
        for j in range(15):
            val = (i + j) % 26
            char = chr(val + 0x40)
            content.append(char)

    inner_content = "".join(content)[:61]
    flag = f"ARA6{{{inner_content}}}"

    return flag

flag = generate_flag()
print(flag)
