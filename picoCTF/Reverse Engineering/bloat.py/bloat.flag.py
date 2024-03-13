import sys

a = (
    "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    + "[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ "
)


def arg133(arg432):
    if arg432 == "h" + "a" + "p" + "p" + "y" + "c" + "h" + "a" + "n" + "c" + "e":
        return True
    else:
        print(
            "T"
            + "h"
            + "a"
            + a[83]
            + a[94]
            + "p"
            + "a"
            + a[82]
            + a[82]
            + a[86]
            + a[78]
            + a[81]
            + a[67]
            + a[94]
            + a[72]
            + a[82]
            + a[94]
            + a[72]
            + "n"
            + "c"
            + a[78]
            + a[81]
            + a[81]
            + "e"
            + "c"
            + a[83]
        )
        sys.exit(0)
        return False


def arg111(arg444):
    return arg122(
        arg444.decode(),
        a[81] + "a" + "p" + a[82] + "c" + "a" + a[75] + a[75] + a[72] + a[78] + "n",
    )


def arg232():
    return input(
        a[47]
        + a[75]
        + "e"
        + "a"
        + a[82]
        + "e"
        + a[94]
        + "e"
        + "n"
        + a[83]
        + "e"
        + a[81]
        + a[94]
        + "c"
        + a[78]
        + a[81]
        + a[81]
        + "e"
        + "c"
        + a[83]
        + a[94]
        + "p"
        + "a"
        + a[82]
        + a[82]
        + a[86]
        + a[78]
        + a[81]
        + a[67]
        + a[94]
        + a[69]
        + a[78]
        + a[81]
        + a[94]
        + a[69]
        + a[75]
        + "a"
        + a[70]
        + a[25]
        + a[94]
    )


def arg132():
    return open("flag.txt.enc", "rb").read()


def arg112():
    print(
        a[54]
        + "e"
        + a[75]
        + "c"
        + a[78]
        + a[76]
        + "e"
        + a[94]
        + a[65]
        + "a"
        + "c"
        + a[74]
        + a[13]
        + a[13]
        + a[13]
        + a[94]
        + "y"
        + a[78]
        + a[84]
        + a[81]
        + a[94]
        + a[69]
        + a[75]
        + "a"
        + a[70]
        + a[11]
        + a[94]
        + a[84]
        + a[82]
        + "e"
        + a[81]
        + a[25]
    )


def arg122(arg432, arg423):
    arg433 = arg423
    i = 0
    while len(arg433) < len(arg432):
        arg433 = arg433 + arg423[i]
        i = (i + 1) % len(arg423)
    return "".join(
        [chr(ord(arg422) ^ ord(arg442)) for (arg422, arg442) in zip(arg432, arg433)]
    )


arg444 = arg132()
arg432 = arg232()
arg133(arg432)
arg112()
arg423 = arg111(arg444)
print(arg423)
sys.exit(0)
