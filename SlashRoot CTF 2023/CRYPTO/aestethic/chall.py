#! /usr/bin/env python3

from binascii import hexlify, unhexlify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from secret import flag
import json
import base64
import os

IV = os.urandom(16)
KEY = os.urandom(16)

GOL = ['pagi', 'malam']
PROD = ['biora', 'kohf', 'gernier']
RATING = [i for i in range(1,6)]

class Sess:
    def encrypt(username,isLogin,getKupon,isMember):
        details = "{" + f"username={username};get_kupon={getKupon};is_member={isMember}" + "}"
        cipher = AES.new(KEY, AES.MODE_CBC, IV)
        enc = cipher.encrypt(pad(details.encode('latin-1'),16,style='pkcs7'))
        return base64.b64encode(json.dumps({
            'secret':hexlify(enc).decode('latin-1'),
            'is_login':isLogin
        }).encode('latin-1')).decode('latin-1')
    
    def decrypt(sess):
        cipher = AES.new(KEY, AES.MODE_CBC,IV)
        ct = unhexlify(json.loads((base64.b64decode(sess)))['secret'].encode())
        pt = unpad(cipher.decrypt(ct),16, style='pkcs7')
        return json.dumps({
            'secret' : pt.decode('latin1'),
            'is_login' : json.loads((base64.b64decode(sess)))['is_login']
        })

class Kupon:
    def gen(golongan, produk, rating, pesan):
        review = {'pesan' : pesan, 'golongan' : golongan, 'produk':produk, 'rating' : rating}
        cipher = AES.new(KEY, AES.MODE_ECB)
        enc = cipher.encrypt(pad(json.dumps(review).encode(),16))
        return hexlify(enc).decode()
    
    def verify(kupon):
        read = unhexlify(kupon.encode())
        cipher = AES.new(KEY, AES.MODE_ECB)
        pt = json.loads(unpad(cipher.decrypt(read),16).decode())
        
        if pt['golongan'] == 'subuh' and pt['rating'] == 5:
            return f"Ini hadiah untukmu : {flag.decode()}"
        else:
            return "Maaf tidak ada hadiah untukmu kawan :("

def gen_Sess():
    return Sess.encrypt('guest', 0, 0, 0)

def register(username):
    if username == 'member357':
        return 0
    
    return Sess.encrypt(username, 1, 1, 1)

def login(sess):
    try:    
        details = json.loads(Sess.decrypt(sess))
    except:
        return "session error"

    secret = details['secret']
    isLogin = details['is_login']

    if isLogin == 1:
        return 1
    elif isLogin == 0 and "member357;get_kupon=1;is_member=1}" in secret:
        return 2
    elif isLogin == 0:
        return 3
    else:
        return 0

def banner():
    print("""
    
    ░█████╗░███████╗░██████╗████████╗███████╗████████╗██╗░░██╗██╗░█████╗░
    ██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔════╝╚══██╔══╝██║░░██║██║██╔══██╗
    ███████║█████╗░░╚█████╗░░░░██║░░░█████╗░░░░░██║░░░███████║██║██║░░╚═╝
    ██╔══██║██╔══╝░░░╚═══██╗░░░██║░░░██╔══╝░░░░░██║░░░██╔══██║██║██║░░██╗
    ██║░░██║███████╗██████╔╝░░░██║░░░███████╗░░░██║░░░██║░░██║██║╚█████╔╝
    ╚═╝░░╚═╝╚══════╝╚═════╝░░░░╚═╝░░░╚══════╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░╚════╝░

    """)

def menu():
    print("""
    Selamat datang di toko pencuci muka aestethic!
    berhubung kami sedang mengadakan promosi kamu dapat menukarkan kupon untuk mendapatkan hadiah menarik
    namun sebelum kamu mendapatkan kupon kamu harus menjadi member dan login terlebih dahulu

    1. Login
    2. Register as Member
    3. Exit

    """)

def main():
    banner()
    while True:
        menu()
        chs_menu = int(input("Your choise : "))
        if chs_menu == 1:
            os.system('clear')
            banner()
            print(f"Silahkan berikan session kamu!\n\njika belum memiliki session kamu bisa menggunakan session ini\n{gen_Sess()}")
            
            login_sess = input("\nsession kamu : ").encode()
            status = login(login_sess)

            if status == 1:
                os.system('clear')
                banner()
                print('Sudah ada yang login ke akun kamu silahkan coba lagi nanti!\n')
            elif status == 2:
                os.system('clear')
                banner()
                print("Hai selamat datang kembali jika ingin mendapatkan hadiahnya silahkan isi rivew terlebih dahulu\n")
                while True:
                    print("  1. Tukar kupon")
                    print("  2. Dapatkan kupon")
                    print("  3. Exit")

                    pilih = int(input("\nKamu ingin melakukan apa ? "))

                    if pilih == 1:
                        kupon = input("Masukkan kupon kamu : ")
                        verify = Kupon.verify(kupon)
                        print(f"\n{verify}")
                    elif pilih == 2:
                        golongan = input("Apakah kamu golongan orang mencuci muka (pagi/malam) ? ")
                        if golongan in GOL:
                            produk = input("Apakah produk yang akan kamu review (biora/kohf/gernier) ? ")
                            if produk in PROD:
                                rating = int(input('berapakah rating yang akan kamu berikan (1-5) ? '))
                                if rating in RATING:
                                    pesan = input('Adakah pesan yang ingin kamu sampaikan ? ')
                                    kupon = Kupon.gen(golongan, produk, rating, pesan)
                                    print(f"\nSilahkan ambil kupon kamu : {kupon}")
                                else:
                                    print("pilihan tidak ada silahkan kembali lagi nanti")
                            else:
                                print("pilihan tidak ada silahkan kembali lagi nanti")
                        else:
                            print("pilihan tidak ada silahkan kembali lagi nanti")
                    elif pilih == 3:
                        exit()
                    else:
                        print("pilihan tidak tersedia")
            elif status == 3:
                os.system('clear')
                banner()
                print(f"Terimakasi sudah datang ke toko kami ini hadiah anda : s.id/YourFlagIsHere, silahkan datang kembali :)")
            else:
                print(status)
        elif chs_menu == 2:
            username = input('Silahkan masukkan username kamu : ')
            new_session = register(username)
            
            if new_session == 0:
                print("Akun ini sudah terdaftar silahkan gunakan akun yang lain!")
            else:
                print(f"Session kamu adalah : {new_session}" )
        elif chs_menu == 3:
            print("bye-bye!")
            exit()
        else:
            print("Pilihan tidak ada pada menu")
        
if __name__ == "__main__":
    main()