import matplotlib.pyplot as plt

coordinates = []
with open("secret_map.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        x, y = line.split()
        # print(f"({int(x[2:], 16)}, {int(y[2:], 16)})")
        coordinates.append((int(x[2:], 16), int(y[2:], 16)))

print(coordinates)

y = [i[0] for i in coordinates]
x = [i[1] for i in coordinates]

y = list(map(lambda x: -x, y))

plt.plot(x, y, "o")
plt.show()
