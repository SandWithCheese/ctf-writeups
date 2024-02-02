import requests

url = "http://165.227.106.113/header.php"

s = requests.Session()
s.headers.update({"User-Agent": "Sup3rS3cr3tAg3nt", "Referer": "awesomesauce.com"})

r = s.get(url)
print(r.text)
