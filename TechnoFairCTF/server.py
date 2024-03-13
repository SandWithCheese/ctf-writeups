from secret import flag,KEY
import hashlib
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import binascii
import random

assert(len(KEY)==16)


barang_merchandise=[
	["Topi","Rp.50.000,000"],
	["Kaos" ,"Rp.200.000,000"],
	["Bendera" , "Rp.999.999.999,000"],
	["Lightstick","Rp.150.000,000"],
	["Jaket", "Rp.250.000,000"]
]
isi=[10000,20000,50000,100000]

def encrypt_data(data,iv):
	cipher=AES.new(KEY,AES.MODE_CBC,iv=binascii.unhexlify(iv))
	data=pad(data,16)
	token=cipher.encrypt(data)
	token=binascii.hexlify(token)
	return iv+token

def registrasi(username,password):
	iv=binascii.hexlify(password[:16].encode())
	hash_password=hashlib.md5(password.encode()).digest()
	hash_password=binascii.hexlify(hash_password).decode()
	data=json.dumps({"username":username,"password":hash_password,"saldo": "{:.3f}".format(0)}).encode()
	token=encrypt_data(data,iv)
	return token

def login(token):
	token=binascii.unhexlify(token)
	iv=token[:16]
	token=token[16:]
	cipher=AES.new(KEY,AES.MODE_CBC,iv=iv)
	data=cipher.decrypt(token)
	data=unpad(data,16)
	try:
		data=json.loads(data)
		return data,binascii.hexlify(iv)
	except:
		print(f"terdapat error pada data : {binascii.hexlify(data).decode()}")
		return "Error","Error"

def menu_toko(data,iv):
	while True:
		print(f"Halo {data['username']}!, apa yang ingin kamu lakukan: ")
		print("1. cek saldo")
		print("2. top-up saldo")
		print("3. beli merchandise")
		print("4. keluar")
		com=int(input("$ "))
		if(com==1):
			print(f"saldo kamu saat ini : {'{:.3f}'.format(float(data['saldo']))}")
		elif(com==2):
			unik=random.randint(0,999)
			print(f"pengen top-up berapa ni bwang")
			print("1. Rp.10.000")
			print("2. Rp.20.000")
			print("3. Rp.50.000")
			print("4. Rp.100.000")
			com=int(input("$ "))
			try:
				total=isi[com-1]+(unik/1000)
				total=str(total)
				print(total)
				total=total.replace('.',',')
				print(f"pembayaran ke gopay dengan nomor 0813-8377-5460")
				print(f"jumlah pembayaran : Rp.{total}")
				print(f"pastikan kamu menyertakan nominal dengan benar agar dapat kami proses")
			except:
				print("Transaksi top-up error")
		elif com==3:
			print("==============Merchandise Store==============")
			for idx,i in enumerate(barang_merchandise):
				print(f"{idx+1}. {i[0]} {i[1]}")
			com=int(input("$ "))
			try:
				harga=barang_merchandise[com-1][1].strip('Rp.')
				harga=harga.replace('.','')
				harga=harga.replace(',','.')
				harga=float(harga)
				if float(data["saldo"])<harga:
					print("Saldo anda kurang, silahkan melakukan top-up terlebih dahulu")
				else:
					data["saldo"]=str('{:.3f}'.format(float(data["saldo"])-harga))
					if(com!=3):
						print(f"{barang_merchandise[com-1][0]} anda akan segera dikirimkan :), terimakasih telah berbelanja")
					else:
						print(f"loh kok malah mau bendera, yaudah ni {flag}")
			except:
				print("input anda tidak valid!")
		elif com==4:
			print(f"terimakasih dan sampai jumpa!")
			print(f"token anda untuk sesi ini {encrypt_data(json.dumps(data).encode(),iv).decode()}")
			break
		else:
			print("input anda tidak valid!")

while True:
	print(f"==============JKT48 Shop==============")
	print(f"1. Login")
	print(f"2. Registrasi")
	print(f"3. Keluar")
	com=int(input("$ "))
	if(com==1):
		token=input("Masukkan token login: ")
		try:
			data,iv=login(token)
			if data=="Error":
				continue
		except:
			print("Token atau kode unik yang anda masukkan tidak valid!")
			continue
		menu_toko(data,iv)
	elif(com==2):
		username=input("Masukkan username: ")
		password=input("Masukkan password (minimal 16 karakter): ")
		if len(password)<16:
			print("password kurang dari 16 karakter, silahkan registrasi ulang")
		else:
			token=registrasi(username,password)
			print(f"gunakan token ini untuk login")
			print(f"token: {token.decode()}")
	elif com==3:
		print("Sayonara~~")
		exit()
	else:
		print("input anda tidak valid!")
