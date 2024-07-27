from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from secret import flag
import hashlib
import os
import random
import string


charset=string.printable



class dh():
    def __init__(self,p,g):
        self.p=p
        self.g=g
        self.privatekey=random.randrange(2,p-1)
        self.pubkey=pow(g,self.privatekey,p)
        self.BLOCK_SIZE=16

    def get_pubkey(self):
        return self.pubkey

    def bytes_to_bin(self,val):
        return "{:08b}".format(bytes_to_long(val))

    def mult_mat(self,a,b,m):
        assert len(a[0]) == len(b)
        return [[sum([int(a[k][i]) * int(b[i][j]) for i in range(len(b))]) % m for j in range(len(a))] for k in range(len(a))]

    def add_mat(self,a,b,m):
        assert len(a[0]) == len(b[0]) and len(a) == len(b)
        return [[(int(a[i][j]) + int(b[i][j])) % m for j in range(len(a[0]))] for i in range(len(a))]

    def hex_to_bytes(self,msg):
        return long_to_bytes(int(msg,16))
    
    def bits_to_matrix(self,val):
        temp=[list(val[i:i+16]) for i in range(0, 256, 16)]
        return temp
    
    def matrix_to_bits(self,val):
        return ''.join(str(i) for j in val for i in j)

    def bytes_to_hex(self,msg):
        return "{0:x}".format(bytes_to_long(msg))


    def generate_secret(self,pub):
        self.sharedsecret=pow(pub,self.privatekey,self.p)
        temp=("{0:b}".format(self.sharedsecret)).rjust(768,'0')
        self.A,self.B,self.C=[temp[i:i+256] for i in range(0,768,256)]
        self.A=self.bits_to_matrix(self.A)
        self.B=self.bits_to_matrix(self.B)
        self.C=self.bits_to_matrix(self.C)

    
    def encrypt(self,msg):
        msg=pad(msg,self.BLOCK_SIZE)
        iv=os.urandom(self.BLOCK_SIZE)
        cipher=AES.new(hashlib.sha256(long_to_bytes(self.sharedsecret)).digest(),AES.MODE_CBC,iv=iv)
        ct=cipher.encrypt(msg)
        return self.bytes_to_hex(ct),self.bytes_to_hex(iv)

    def decrypt(self,enc,iv,sig):
        cipher=AES.new(hashlib.sha256(long_to_bytes(self.sharedsecret)).digest(),AES.MODE_CBC,iv=self.hex_to_bytes(iv))
        try:
            pt=unpad(cipher.decrypt(self.hex_to_bytes(enc)),self.BLOCK_SIZE)
            verif=(self.hash(pt)==sig)
            return verif,pt.decode()
        except:
            return False,''

    def hash(self,msg):
        len_msg=len(msg)
        msg=self.bytes_to_bin(msg)
        if(msg[0]=='0'):
            val=self.mult_mat(self.A,self.C,2)
        else:
            val=self.mult_mat(self.B,self.C,2)
        msg=msg[1:]
        for i in msg:
            if int(i)==0:
                val=self.mult_mat(self.mult_mat(val,self.A,2),self.C,2)
            else:
                val=self.mult_mat(self.mult_mat(val,self.B,2),self.C,2)
        val=self.add_mat(val,self.C,2)
        sig=self.matrix_to_bits(val)
        return "{:x}".format(int(sig))

    def kirim(self,msg):
        sig=self.hash(msg)
        enc,iv=self.encrypt(msg)
        return enc,iv,sig


        
if __name__=='__main__':
    p=getPrime(768)
    g=8
    print('Yujin sending modulo and base')
    print(f'Modulo  : {p}')
    print(f'g       : {g}')
    print('Able to change modulo')
    try:
        inp=input("> ")
        temp=len("{:08b}".format(int(p)))
        if(temp>=512 and temp<=768):
            pass
        else:
            print('Invalid value sending as it is')
        p=int(inp)
    except:
        pass
    B=dh(p,g)
    print("Marsha sending public key...")
    print(f"Sucessfully intercepted Marsha's public key")
    print(f"Marsha's public key : {B.get_pubkey()}")

    A=dh(p,g)
    A.generate_secret(B.get_pubkey())
    print("Yujin sending public key...")
    print(f"Sucessfully intercepted Yujin's public key")
    print(f"Yujin's public key : {A.get_pubkey()}")

    B.generate_secret(A.get_pubkey())
    enc,iv,sig=B.kirim(b"Halo, kamu apa kabar?")

    print(f"Successfully intercepted Marsha's message")
    print(f'enc          : {enc}')
    print(f'iv           : {iv}')
    print(f'signature    : {sig}')
    try:
        print("Able to change Marsha's encrypted message")
        inp1=input("> ")
        enc=int(inp1,16)
        enc="{:x}".format(enc)
    except:
        print('Invalid value sending as it is')
        pass
    
    verif,pt=A.decrypt(enc,iv,sig)
    try:
        assert all(i in charset for i in list(pt))
    except:
        print('Yujin left the chat...')
        exit()
    if(not verif):
        print('Yujin left the chat...')
    elif pt!="Halo, kamu apa kabar?":
        if verif:
            enc,iv,sig=A.kirim(flag)
            print(f"Successfully intercepted Yujin's message")
            print(f'enc          : {enc}')
            print(f'iv           : {iv}')
            print(f'signature    : {sig}')
        else:
            print('Yujin left the chat...')

    else:
        enc,iv,sig=A.kirim(b"Aku baik, bentar ya aku tidur dulu...")
        print(f"Successfully intercepted Yujin's message")
        print(f'enc          : {enc}')
        print(f'iv           : {iv}')
        print(f'signature    : {sig}')
        print(f"Yujin left the chat...")
    
    


    
    
    

    