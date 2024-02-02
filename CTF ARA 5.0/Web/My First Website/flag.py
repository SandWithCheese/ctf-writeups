import requests
import urllib3

url = "http://103.152.242.68:10012"

s = requests.Session()


req = s.get(
    url + "/environment",
    # headers={"X-Forwarded-For": "127.0.0.1"},
    proxies={"http": "http://127.0.0.1"},
    params={"admin": "daffainfo"},
)

print(req.text)
