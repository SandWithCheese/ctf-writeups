from random import randrange


A = randrange(1000000000)
B = randrange(1000000000)
C = randrange(1000000000)
D = randrange(1000000000)
M = 6507347070768067803177302629220355584585341427822710449

seq = [randrange(1000000000), randrange(1000000000), randrange(1000000000), randrange(1000000000)]

def aha(n):
    res = seq
    for i in range(len(res), n + 1):
        res.append((res[i - 4] * A + res[i - 3] * B + res[i - 2] * C + res[i - 1] * D) % M)
    return res

def ehe(a):
    return (a[-1] * a[-2]) ^ (a[-3] * a[-4])


creds = 'ln_y{' + ''.join(str(x)[1::2] + str(x)[::2] + '_' for x in aha(10))[:-1] + '}'
print(f'creds:', creds)


password = 0
for i in range(1, 10):
    password ^= ehe(aha(1111111111111111111111111111111111111 * i)[::69])

checker = int(input('infokan password kaks.... hihihi :V\n'))
if checker != password:
    print('\nkamu bukan orang yang aku kenal >:(')
else:
    with open("flag.txt", "rb") as file:
        flag = file.read().strip()
        file.close()

    print('\nehehe~ ahaha~ nih hadiah ^_^')
    print(flag)