from Crypto.Util.number import getPrime

def generate_rsa_keys(bits=1024, e=3):
    while True:
        p = getPrime(bits // 2)
        q = getPrime(bits // 2)
        n = p * q
        phi = (p - 1) * (q - 1)
        if phi % e != 0:
            break
    d = pow(e, -1, phi)
    return ((e, n), (d, n))

def cube_root(n):
    lo = 0
    hi = n
    while lo < hi:
        mid = (lo + hi) // 2
        if mid ** 3 < n:
            lo = mid + 1
        else:
            hi = mid
    return lo