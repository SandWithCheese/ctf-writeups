bound1 = 1295911241295070912759062510927419182371092570912740917209471290749986192846891264891628946189264982
bound2 = 9124789812750912709571902562640812649812640812640126508126408612084612856193641021290712049605126091
bound3 = 5275097124129650129640129471209719207491206751249012709217590109128390127490172599471092650192750500


def eq1(x):
    return x + 2


def eq2(x):
    return 3 * x**2 + x + 5


def eq3(x):
    return 69 * x**4 + 420 * (x + 69) ** 2 + 420 * x


# 2*n + (n(n+1)/2)
def eq1_eval(n):
    ret = (2 * n) + (n * (n + 1) // 2)
    return ret % (bound1 * bound2)


# 5*n + (n(n+1)/2) + 3(n(n+1)(2n+1)/6)
def eq2_eval(n):
    ret = (5 * n) + (n * (n + 1) // 2) + (3 * (n * (n + 1) * ((2 * n) + 1) // 6))
    return ret % (bound1 * bound3)


# 420*(n(n+1)/2) + 420*(n(n+1)(2n+1)/6) + 69*((6n^5+15n^4+10n^3-n)/30)
def eq3_eval(n):
    ret = (
        (420 * (n * (n + 1) // 2))
        + (420 * ((n + 69) * (n + 1 + 69) * ((2 * (n + 69)) + 1) // 6))
        + (69 * ((6 * n**5 + 15 * n**4 + 10 * n**3 - n) // 30))
        - (420 * (69 * (69 + 1) * ((2 * 69) + 1) // 6))
    )
    return ret % (bound2 * bound3)


eval_pad1 = str(
    eq1_eval(91826498126598612984698126498162984698215011028470182748192650182640812648)
    * pow(10, 40)
)
eval_pad2 = str(
    eq2_eval(61984698126481720571290471920740912759102874091264012640861208461826012842)
    * pow(10, 80)
)
eval_pad3 = str(
    eq3_eval(53289653298649832498103841081365081364802478126583016583160568136501681357)
    * pow(10, 160)
)

key1 = bytearray([int(eval_pad1[i : (i + 4)]) & 127 for i in range(0, 40, 4)])
key2 = bytearray([int(eval_pad2[i : (i + 4)]) & 127 for i in range(0, 80, 4)])
key3 = bytearray([int(eval_pad3[i : (i + 4)]) & 127 for i in range(0, 160, 4)])

with open("enc.txt", "r") as file:
    enc = file.readline()

dec = (
    "".join([chr(ord(enc[0:10][i]) ^ key1[i]) for i in range(0, len(key1))])
    + "".join([chr(ord(enc[10:30][i]) ^ key2[i]) for i in range(0, len(key2))])
    + "".join([chr(ord(enc[30:70][i]) ^ key3[i]) for i in range(0, len(key3))])
)

print(dec)
