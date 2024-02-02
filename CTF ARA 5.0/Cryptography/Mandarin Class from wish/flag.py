enc = "㭪䫴㭪ひ灮带⯠⯠孨囖抸櫲婾懎囖崼敶栴囖溚⾈牂"

for i in range(1, 501):
    flag = ""
    for ch in enc:
        flag += chr(ord(ch) // i)
    
    if "ARA" in flag:
        print(flag)