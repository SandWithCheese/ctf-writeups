decrypted = "xk|nF{quxzwkgzgwx|quitH"

# main
# for (i = 0; i < 23; i = i + 1) {
#     cVar1 = complex((int)local_28[i],(int)local_28[i],2,0xab7490fe,param_5,param_6,param_2);
#     local_28[i] = cVar1;
#     cVar1 = complex2((int)local_28[i],(int)local_28[i],local_28[i] + -1);
#     local_28[i] = cVar1;
# }

# complex
# if ((64 < param_1) && (param_1 < 126)) {
#     local_c = (param_2 + 65) % 122;
#     if (local_c < 65) {
#       local_c = local_c + 61;
#     }
#     return local_c;
# }

# complex2
# local_c = (param_2 + 65) % 122;
#   if (local_c < 65) {
#     local_c = local_c + 61;
#   }
# return local_c;


def complex(a):
    if 64 < a < 126:
        c = (a + 65) % 122
        if c < 65:
            c += 61

        return c


def complex2(a):
    c = (a + 65) % 122
    if c < 65:
        c += 61

    return c


flag = ""
for char in decrypted:
    for i in range(65, 126):
        flag_char = i
        temp = complex(flag_char)
        temp = complex2(temp)
        if temp == ord(char):
            flag += chr(flag_char)
            break

print(flag)
