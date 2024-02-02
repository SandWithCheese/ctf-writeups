import requests

url = "https://uoftctf-no-code.chals.io/execute"

s = requests.Session()
r = s.post(url, data={"code": "面積\t"})

print(r.text)
