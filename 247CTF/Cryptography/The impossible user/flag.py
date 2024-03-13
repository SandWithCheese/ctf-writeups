import requests
from binascii import hexlify

url = "https://417df8e45188a611.247ctf.com/"
encrypt_url = f"{url}encrypt?user="
get_flag_url = f"{url}get_flag?user="

flag_user = hexlify(b"impossible_flag_user").decode()
print(flag_user)
print(len(flag_user))

print(bytes.fromhex(flag_user))

s = requests.Session()

payload = "0c" * 12
# payload = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
print(len(payload))
print(s.get(url=f"{encrypt_url}{flag_user}{payload}").text[:64])
# print(s.get(url=f"{encrypt_url}{payload}").text)

flag = "939454b054b7379b0709a270b894025c707ece4f0913868ec5df07d131b0822d"
print(s.get(url=f"{get_flag_url}{flag}").text)
