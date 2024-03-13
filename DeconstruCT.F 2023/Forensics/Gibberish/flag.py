with open("flag.txt", "r") as f:
    datas = f.readlines()

# stripped_data = ""
# print(datas)
stripped_datas = []
for data in datas:
    new_data = ""
    for char in data:
        if char != "A" and char != "\n":
            new_data += char
    if new_data != "":
        stripped_datas.append(new_data)

print("".join(stripped_datas))
# for char in data:
#     if char != "A":
#         stripped_data += char

# print(stripped_data)
