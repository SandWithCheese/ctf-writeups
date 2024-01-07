#!/usr/bin/env python3

def check_flag(flag):
	enc_flag = [110, 102, 118, 102, 115, 114, 118, 130, 103, 104, 92, 80, 98, 108, 63, 63, 65, 112, 113, 144]

	if len(flag) != len(enc_flag):
		return False

	for i,j in enumerate(flag):
		if ord(j)+i != enc_flag[i]:
			return False
	
	return True

def main():
	flag = input("[>] Insert Flag: ")
	check = check_flag(flag)

	if check: print("[*] Flag Benar!")
	else: print("[*] Flag Salah!")

if __name__ == '__main__':
	main()