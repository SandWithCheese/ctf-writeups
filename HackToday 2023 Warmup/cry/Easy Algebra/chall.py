from Crypto.Util.number import *
import random

whatisthis = [1]

def just(a: int, b: int) -> int:
    result = whatisthis[a]//(whatisthis[b]*whatisthis[a-b]) 
    return result

def baby(a: int, b: int, n: int) -> int:
    gift = 0
    for i in range(n+1):
        if abs(n - 2*i) != 13:
            continue
        gift += just(n,i)*pow(a,i)*pow(b,n-i)
    return gift

def algebra(txt: str) -> tuple:
    with open(txt,"rb") as f:
        m = f.read().strip()
        m = bytes_to_long(m)
        e,p,q = 65537,getPrime(1024),getPrime(1024)
        f.close()
    return (m, e, p, q)
 
def okay():
    u = random.randint(10, 1000)
    v = random.randint(10, 1000)
    w = getPrime(random.randint(5,9))
    return u, v, w

def easy(w):
    global whatisthis
    [whatisthis.append(i*whatisthis[-1]) for i in range(1,w+1)]

def apanih(n,e,c,x):
    with open("output.txt","w") as f:
        output = f"{n = }\n"
        output += f"{e = }\n"
        output += f"{c = }\n"
        output += f"{x = }\n"
        f.write(output)
        f.close()

def main():
    m,e,p,q = algebra("flag.txt")
    n = p*q
    c = pow(m,e,n)
    u,v,w = okay()
    easy(w)
    x = baby(p*u*7,-(q*v)*3,w)
    apanih(n,e,c,x)

if __name__ == "__main__":
    main()