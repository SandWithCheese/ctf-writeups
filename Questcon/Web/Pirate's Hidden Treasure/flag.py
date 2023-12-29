import requests

url = "https://questcon-pirate-treasure.chals.io/"
headers = {
    "User-Agent": "pirate browser",
    # "Origin": "Black Perl",
    # "referer": url,
    # "date": "2018-04-01'",
    # "DNT": "1",
    # "X-Forwarded-For": "31.3.152.55",
    # "Accept-Language": "sv,en;q=0.9",
}

s = requests.Session()
request = s.get(url, headers=headers)

print(request.text)

s.close()
