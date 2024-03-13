def matrix2bytes(matrix):
    """Converts a 4x4 matrix into a 16-byte array."""
    pl = ""
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            pl += chr(matrix[i][j])
    return pl


state = [
    [206, 243, 61, 34],
    [171, 11, 93, 31],
    [16, 200, 91, 108],
    [150, 3, 194, 51],
]

round_key = [
    [173, 129, 68, 82],
    [223, 100, 38, 109],
    [32, 189, 53, 8],
    [253, 48, 187, 78],
]


def add_round_key(s, k):
    round_key = []
    for i in range(len(s)):
        row = []
        for j in range(len(s[i])):
            row.append(s[i][j] ^ k[i][j])
        round_key.append(row)
    return round_key


print(matrix2bytes(add_round_key(state, round_key)))
