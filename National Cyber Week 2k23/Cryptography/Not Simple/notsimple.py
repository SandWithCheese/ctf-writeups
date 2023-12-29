from Crypto.Util.number import *
from Crypto.Util.Padding import *
import string
import random
import time
from secrets import FLAG


def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def enc1(kode):
    m = bytes_to_long(kode.encode())
    p,q = getPrime(600),getPrime(600)
    n = p*q
    opr1 = inverse(pow(p,5),q)
    opr2 = (pow(p,7,n) - pow(q,65537,n)) % n
    c = pow((pow(opr1 * m * opr2, 65537, n) * pow(inverse(opr1,n),2,n) * pow(inverse(opr2, n),3,n)) % n,3,n)
    return n,65537,opr1,opr2,c

def wow():
    wow = [random.getrandbits(32) << (128*pow(2,i)) for i in range(0, 4)]
    wadidaw = 0
    for i in wow:
        wadidaw |= i
    return wadidaw

def enc2(opr1,opr2,e,p,q):
    n = p*q
    c = pow(bytes_to_long(long_to_bytes(opr1) + b'bebek' + long_to_bytes(opr2)) + wow(), e, n)
    return c,n,e

kode = generate_random_string(50)
n1,e1,opr1,opr2,c1 = enc1(kode)

e = input("Masukkan e = ")
foul = 0
while e.isdigit() == 0 or int(e) % 2 == 0 or int(e) <= 13:
    foul += 1
    print("Masukkan lagi")
    e = input("Masukkan e = ")
    if(foul == 3):
        print("Males sayah..")
        exit(0)


p,q = getPrime(1024),getPrime(1024)
e = int(e)

while True:
    print("""
         1. Liat nilai wadidaw
         2. Melihat enkripsi dari kode1 dan kode2
         3. Input kode1 and kode2
         4. Exit
          """)
    choose = input(">> ")
    if choose == "1":
        print(f'Nilai wadidaw = {hex(wow())}')
    elif choose == "2":
        c2,n2,e2 = enc2(opr1,opr2,e,p,q)
        print(f'c = {c2}')
        print(f'n = {n2}')
        print(f'e = {e2}')
    elif choose == "3":
        init = time.time()
        cobaopr1 = input("opr1 = ")
        cobaopr2 = input("opr2 = ")
        try:
            if (time.time() - init > 15):
                print(f"waktu anda kelamaan {time.time() - init}")
                exit()
            elif int(cobaopr1) == opr1 and int(cobaopr2) == opr2:
                print("Nice, skarang lagi satu tebak kode berikut")
                print(f'n = {n1}')
                print(f'e = {e1}')
                print(f'c = {c1}')
                cobakode = input("Kode = ")
                if (time.time() - init > 15):
                    print(f"waktu anda kelamaan {time.time() - init}")
                    exit()
                elif cobakode == kode:
                    print(f"Dahlah, gw dah capek {FLAG}")
                else:
                    print("Nope")
                    exit()
            else:
                print("Nope")
                exit()
        except:
            print("Nope")
            exit()
    elif choose == "4":
        print("bye!!")
        exit()
    else:
        print("We..")
        exit()


