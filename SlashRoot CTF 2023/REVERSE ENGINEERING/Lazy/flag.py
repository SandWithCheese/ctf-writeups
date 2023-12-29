from string import ascii_lowercase, ascii_uppercase, digits, punctuation

# fake_flag = "fakeflag{hai}\0"
flag = "119 107 99 108 124 96 99 104 120 121 105 99 120".split()

# for i in range(len(flag)):
#     print(ord(fake_flag[i]) ^ 2)

flag = "119 112 51 108 97 85 52 108 112 85 122 52 102 54 55 106 85 113 51 108 85 104 104 52 105 113 51 76 124 48 112 101 101 114 108 113 99 104 113".split()
text = ascii_uppercase + ascii_lowercase + digits + "{}"
text_lookup = "119 124 62 63 48 49 50 51 52 53 54 55 125 126 127 109 110 111 112 113 114 115 116 101 102 103 104 105 106 107 108 96 120 121 122 97 98 99 93 94 95 77 78 79 80 81 82 83 84 69 70 71 72 73 74 75 76 64 88 89 90 65 66 67".split()

for i in range(len(flag)):
    print(text[text_lookup.index(flag[i])], end="")
# for i in range(len(text_lookup)):
#     # print(text_lookup[i])
#     if chr(int(text_lookup[i])) == "a":
#         print(i)
#         break

# for i in range(len(text)):
#     if text[i] == "a":
#         print(text_lookup[i])
#         break
