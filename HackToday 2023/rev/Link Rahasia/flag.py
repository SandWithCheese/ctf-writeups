arr = [
    0,
    23,
    0,
    29,
    4,
    29,
    27,
    1,
    0,
    9,
    22,
    0,
    4,
    28,
    7,
    6,
    19,
    24,
    12,
    24,
    20,
    6,
    10,
    28,
    14,
    16,
    23,
    21,
    14,
    1,
    23,
    6,
    4,
    19,
    23,
    0,
    0,
    8,
    7,
    25,
    5,
    8,
    12,
    11,
    9,
    9,
    2,
    16,
    24,
    28,
    17,
    2,
    20,
    10,
    24,
    5,
    4,
    23,
    23,
    17,
    9,
    14,
    14,
    15,
    4,
    11,
    23,
    1,
    25,
    12,
    1,
    4,
    19,
    22,
    3,
    25,
    25,
    22,
    16,
    28,
    4,
    24,
    6,
    10,
    19,
    21,
    14,
    7,
    19,
    19,
    22,
    2,
    24,
    23,
    19,
    15,
    4,
    3,
    28,
    20,
    19,
    3,
    26,
    27,
    19,
    2,
    4,
    18,
    15,
    3,
    10,
    22,
]

b = []

# Step 1
# for (int i = s.length() - 1; i >= 0; --i) {
#             int char1 = s.charAt(i);
#             for (int j = 0; j < 7; ++j) {
#                 this.b.add(char1 % 2);
#                 char1 /= 2;
#             }
#         }
#         Collections.reverse(this.b);

for i in range(len(arr) - 1, -1, -1):
    char1 = arr[i]
    for j in range(7):
        b.append(char1 % 2)
        arr[i] /= 2

# print(b)
# print(arr)

# Step 2
# public int b(final int n) {
#     int n2 = 1;
#     int n3 = 0;
#     for (int i = n + 27; i >= n; --i) {
#         n3 += this.b.get(i) * n2;
#         n2 *= 2;
#     }
#     return n3;
# }

n2 = 1
n3 = 0
for i in range(n+27, n-1, -1)
