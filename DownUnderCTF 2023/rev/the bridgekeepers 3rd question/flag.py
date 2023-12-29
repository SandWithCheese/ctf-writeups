a = [] 
b = [] 
c = [] 
d = [] 
e = [] 
f = [] 
g = [] 
h = [] 
i = [] 
j = [] 
k = [] 
l = [] 
m = []
n = "blue"

a.extend([a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, a, b, a, a, a, a, a, a, a, a])
b.extend([b, b, b, b, c, b, a, a, b, b, a, b, a, b, a, a, b, a, b, a, a, b, a, b, a, b])  
c.extend([a, d, b, c, a, a, a, c, b, b, b, a, b, c, a, b, b, a, c, c, b, a, b, a, c, c])
d.extend([c, d, c, c, e, d, d, c, c, c, c, b, c, c, d, c, b, d, a, d, c, c, c, a, d, c])
e.extend([a, e, f, c, d, e, a, e, c, d, c, c, c, d, a, e, b, b, a, d, c, e, b, b, a, a])
f.extend([f, d, g, e, d, e, d, c, b, f, f, f, a, f, e, f, f, d, a, b, b, b, f, f, a, f])
g.extend([h, a, c, c, g, c, b, a, g, e, e, c, g, e, g, g, b, d, b, b, c, c, d, e, b, f])
h.extend([c, d, a, e, c, b, f, c, a, e, a, b, a, g, e, i, g, e, g, h, d, b, a, e, c, b])
i.extend([h, a, d, b, d, c, d, b, f, a, b, b, i, d, g, a, a, a, h, i, j, c, e, f, d, d])
j.extend([b, f, c, f, i, c, b, b, c, j, i, e, e, j, g, j, c, k, c, i, h, g, g, g, a, d])
k.extend([i, k, c, h, h, j, c, e, a, f, f, h, e, g, c, l, c, a, e, f, d, c, f, f, a, h])
l.extend([j, k, j, a, a, i, i, c, d, c, a, m, a, g, f, j, j, k, d, g, l, f, i, b, f, l])
m.extend([c, c, e, g, n, a, g, k, m, a, h, h, l, d, d, g, b, h, d, h, e, l, k, h, k, f])

walk = a

# print(walk[17][4][1][1][0][4][-7][-7][9][1][-1][8])
# print(walk[17][4][1][1][0][4][-7][-7][9][1][-1])
print(walk[17][4][1][4][2][2][0][15][20][17][15][11][4])
# print(walk[17][4][1][4][2])

target = [17, 4, 1, 4, 2, 2 ,0 ,15, 20 ,17 , 15, 11, 4]
payload = []
for i in target:
    payload.append(chr(i + 97))

print("".join(payload))

# for i in range(len(walk)):
#     for j in range(len(walk[i])):
#         try:
#             if walk[i][j] == "blue":
#                 print(i, j)
#         except:
#             pass

# print(a.index("blue"))