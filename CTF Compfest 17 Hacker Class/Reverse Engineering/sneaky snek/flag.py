charset = "2sYvjWMlXF73bRUOHeTVnZ8gquP9Dtd0cxEp5raJKoI4SyNA6hfwmiGLBzkQ1C"

# Extracted `fucky` values (just show how to process one for now)
chunks = (
    "4LAKsvB\x02\x10tPGYCQVk\x06n2\x1c\x10\x11Zl\x05\x10U\x06ehNjmycuH8Mbz7rFRxoOE\x11fD9aqS5i1Ww\x1eJg36X\x16TpI0",
    "gljrHw\x035Dc\x16GTzU49F7IniObX\x01oY\x13m\x14x6aRQWqk\x12M0Z\x16yCK81ePVvd\x04tpAJ\x0cSE\x18LsfhuB\x0e\x1b2N",
    "qiW5MbaOEGI\x0flerU\x07oJn\x01\x17kKS3QD\x15hYCVst96FmAd\x0cwLuv\x002xRPX\x19\x13yf\x19\x157j4ZT\x02B1gp8zN0H",
    "eTk350Fj\x02OR\x16wYPlxzpU\x17\x121Z\x0bXc84VHrmI2y\x1b\x0faAG\x06LdWNSi\x0fsCDu9M\x12hn\x12gqtKbBv\x1eEQf7J6",
    "K\x1bGPaj9\nloF5w8DO\x18qI\x05LiZe\x03v\tR21\x0f\x08YzcCyVp6W\x0ebNXxB3AJkEQSug\x03sM\x07rn\x1dTf4d0Hht7U",
    "DrAUWfsoPwnBJQbEzhMYH\x1bTlvG579RS3jcIa\x0f\x0eudO\x0fF\x12eV\x1702\x11CN\x008t\x021mXxLy4\x05qkK\x1b\ri6gZ",
    "\x15xKDwaU3705Qo8\x1a\x1bgvhBT2VR\x0bINPk\x02\x11JtcG4OCqMj\x0e\x04e9i\x1asflu\x1bYymEdSb\rzXLW\x036HpFAZrn",
    "87xEb\x11\x0fmQp\rP\x0cGfDg\x18qdy6X4RU01u\x13ztsic\x105n\x0fOv\x0f\x1dkeZFwT9oMCBYVA\x1cr2\x0bHSJjIaW3hKLN",
    "wO\t\x14\x17rx5KzD\x04dRvF\x196\x1bMyaAXqfGl1tTs4\x12o78nLBCSVYhJ9UgjNu3cE\x14ZbW\x1aQ20mkHIi\x19p\x1e\x1dP",
    "6\x08\x16q0oje\x05a9PKYCTb\x0f\x1bO\x045JgfwQi4D\x1b2h3HzvElBZLskxFnd8WIA\x0e\x05MS\x03uRpXmG1VNcy\x19\x1c7tU",
    "7Mi\x18\x01lqugN\t\x0bVC\x0c\x01KoQ\x18vAH\x0bOB29c1\x1d0hrd\x12jwRTaYXIGUFfmzEL6kS8yne53bPJWDxZ\x0ft\rp4",
    "RcVWC\x19\x1cxDd9v7L2kS4\x14f0Im\x1agqst\x15\x10\x0ebBny86rh\x10wl\x1dHOa5NpQjUuKEeTzA1\x0cYXMFP\x1bJoiG3\x00Z",
    "5ch\x02e\x15I\x04KNrQVu\x00OmYG8F\x13n\x1cdgAED\x1dtpz0fTBWUCS\x07wv9bklyXP\x17RL\x0fMZH3qsa1\x1cxj\x0b672oiJ",
    "U\x01P\x14znLCeX\x11kJ6NEv\x1eD\nQfKYow\nidl742c\x05h5Z\x10jMW\x11bS8gyR1qtOGF\nxpT9Bu\x07s3H\x1d0IVmaA",
    "\x07dwezE8SUaCl\x15bmIWfsLY6vM\x05c\x02tDK\x13nP\x1cOGZ4jhp\x00Xk0Txo\x1byB9RA15F\x00JV\x042qguNr7\x08HiQ\x13",
    "AH\x01BgpyC7uT\n24\x17P5KM\x18\x1do36hQV\x02a\x03bvNW9cJzRZIqF\x06\x12EmfY1esX\x0f\x0e8irj\tLwlUnGDdSxkt0O",
    "9\x19\x070ymL\x14xlvJ\x0fh4\x13ZB8tRHfwpFEeMCo37qdgkQ\x17cWUj1\x11\x1eIzK6X5\x01iaTY\x1brOPNb2SGs\x13\x0cVAuD",
    "\r1OZ\x01cn\x16Cdfxeo2SFJ9s3iUvzaYX7\x198DhTL\x1bmBGprNAPEMVw5q4kg\nlu\x1dRKyI\r\x05bjWt\x176H\x01Q\x19",
    "V\x01R\x13bQo8\n\x060hmdZ\nAKu7N1fP\x03EX\rIsBGxjiM3ary5\x16WqD2\x07zJ9\nvlnwc\x12kYg\x066COeTpHSFUL4",
    "csrl\x13P\x1c\x1azJ0\x1aMtRdBuVCFw\x18OW\x0eofYm\x1e\x0b4L\x1b32\x108TAIkx\x19hqg6DN95ijaQUH7pS\x11vebXEyZKnG1",
    "3TF\x17sLv\x10\x13ei\x07KjUSDO56Ju\x1bV\x03PB\x18HC\x08a21yAocbQ97kW0xpENmltd4\x07Z8rRfX\x1dh\x11qYgM\x04GnzI",
    "HBsjVRFD1P3T\x07Ktod\x11yaM\x07Jn\x0eu\tzbgSw95qCf72W6pkYr\x13iE\x04cAmQ\x0bxZ\x16vNUlGO4L\x110I\x16e\x148X",
    "SyrM89un\x14lJ6DY\x13\x18x\t\x1cBfhkCipaIGvZ\n5zK1V2qjc\x14XOetUgP70\x14FwW\x10\x10\x0coTmNbERsA3Q\x1dLHd",
    "qUZFm\x1a\x12G6pIE\nT\x04v\x19f\x0c0C5\x00z\x06iMWrtXlDwLdPV9Oy\x0e3NAon\x1d8bes\x1aaJHYc1gjSRxQKB24uhk\x16",
    "pcaRTFJu1Lh4\x0fzNeHg6viVmb\nM\x0eKPW25wDZ\x19\r3UGOqA\x1b\x02\x06r\x07o\x08ClE98s7x\x0eyYd\x05k0QnIXBSjtf",
    "z\x16nrQUaTle0fuZ\x18\x0fLGN8hOXFRYAysE\x0fkJ\x0053Bq4IKb1\x1bCPDdiw\x0ccWg\x0f92m\n\x18x\x086SvoHVtp\x1djM",
    "o\n\x14jf3Z7c\x0flBwg4\x0fmdu9\x06W\x08Jr0Kvipy6TNFxIC8\x02tV\x11MLQ\x1anY\x00\x01OUksz\x1bDG1beHEXPq5RaS2A",
    "1t\x0eso\x1dykB\x0bWCvSwPpbr\x04T4YjmV0hMeXd\x0fi6I\x00xKDcf\x18ulAgn8a\x0f\x1dON5R\x13QJE9LqFHUZ\x04\x03Gz72",
    "DItwxnU72\x1e6\x02b8r\x1e\x06HKQiB\x0cPZsOcu\x0bC5RXSLA0oNM\x11\x029JgmzvTh4\x063\x19\x08pFY\x1bVa1dlqjGWeEkf",
    "\x10BVsurx\x12OAtMX6\x19qmKjHpd3b1\x04f\x07i\x01aoCInLZSNQ9Fl2R\x01\x1a4Jvz0h\x18\x068GP5\x0eeUc\rEWyTDwk7Yg",
    "a\x08yQruNhmT\x074WeCMv7\x00K2x\x14oL3GFElnDX\x03\x1d\x03S\x10c\nt9pijfYUI80AqOgR5\x12\x0ezPHV6\x1eBkdwJZ1b",
    "NygB\x15A5\x150nZojRPe79YKwu\x14JEXSI1tpivFmxV4\x1d\x1c\x14\x18\nk\x00lOqMWDGLs\x0bfhU8Q\x1e\x0cb2HcrzTaCd6",
    "\x1c\x18\x021\x074QixUE6ZTtG\x04Rp7vnjAYrB80yNXszeqawL9Oc\x07goHbufCV\x1cP\x1ahMIl\x16F52\x0fKdWkJmD\x11S\n",
    "\n9\x1dHxQ\x1bqRjo\x0ekz5gZ4VMuFeYb\x18ywN\x1aJrL\x01cXi8KTd1\nW6IDa\x08sphtABEP3\nUv7\x1en0lOCf\x14GS2",
)

flag = []

for idx, chunk in enumerate(chunks):
    temp = charset
    for ch in chunk:
        temp = temp.replace(ch, "")
    if len(temp) == 1:
        flag.append(temp)
    elif len(temp) == 0:
        flag.append("_")
    else:
        print(f"Unexpected temp: idx={idx}, temp={temp}")
        break

flag = "".join(flag)

from hashlib import sha256

hsh = sha256(flag.encode()).hexdigest()[:10]
print(f"COMPFEST17{{{flag}_{hsh}}}")
