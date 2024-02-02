from collections import Counter

with open("data.dat", "r") as f:
    datas = f.readlines()

count = 0
for data in datas:
    obj = list(data.strip())
    obj = Counter(obj)
    if obj["0"] % 3 == 0 or obj["1"] % 2 == 0:
        count += 1

print(count)
