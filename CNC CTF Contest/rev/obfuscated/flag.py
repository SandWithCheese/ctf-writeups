from string import printable

obs_flag = """65
52
22
226
178
3
137
249
54
19
41
244
148
114
132
195
104
53
35
223
185
52
129
217
93
80
62
199
215
47
183
195
102
5
96
201
128
20
129
255
58
47
2
244
174
32
154
253
35
29
""".split()

for char in printable:
    flag_format = "CTFITB{" + char

    xor_values = []
    for i in range(len(flag_format)):
        xor_values.append(int(obs_flag[i]) ^ ord(flag_format[i]))

    for i in range(len(obs_flag)):
        print(chr(int(obs_flag[i]) ^ xor_values[i % 8]), end="")

    print()
