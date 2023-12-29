with open("he.txt", "r") as f:
    he = f.read().split()

with open("she.txt", "r") as f:
    she = f.read().split()

diffs = []
for i in range(len(he)):
    if he[i] != she[i]:
        diffs.append([he[i], she[i]])

flag = "4wes0M3_sTories_man"