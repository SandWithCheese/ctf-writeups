import random
from random import randint

flag = "???"

encrypted_flag = ""

key = randint(1,500)

for ch in flag:

    e = chr(ord(ch)*key)
    encrypted_flag += e

print(key)
print(encrypted_flag)

# print(key) = ???
# print(encrypted_flag) = "㭪䫴㭪ひ灮带⯠⯠孨囖抸櫲婾懎囖崼敶栴囖溚⾈牂"