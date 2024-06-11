lookup1 = "\n \"#()*+/1:=[]abcdefghijklmnopqrstuvwxyz"
lookup2 = "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrst"

def encrypt(plaintext):
    out = ""
    prev = 0
    for char in plaintext:
        cur = lookup1.index(char)
        out += lookup2[(cur - prev) % 40]
        prev = cur
    return out

decrypted_flag = "DLSeGAGDgBNJDQJDCFSFnRBIDjgHoDFCFtHDgJpiHtGDmMAQFnRBJKkBAsTMrsPSDDnEFCFtIbEDtDCIbFCFtHTJDKerFldbFObFCFtLBFkBAAAPFnRBJGEkerFlcPgKkImHnIlATJDKbTbFOkdNnsgbnJRMFnRBNAFkBAAAbrcbTKAkOgFpOgFpOpkBAAAAAAAiClFGIPFnRBaKliCgClFGtIBAAAAAAAOgGEkImHnIl"

flag = ""
for _ in range(len(decrypted_flag)):
    for char in lookup1:
        if decrypted_flag.startswith(encrypt(flag + char)):
            flag += char
            break

print(flag)