p = 29

residue = []
for i in range(29 // 2):
    residue.append(pow(i, 2, 29))
    print(f"{i}: {pow(i, 2, 29)}")

print(sorted(residue))
