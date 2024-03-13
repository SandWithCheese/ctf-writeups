# alphabet = "0fkdwu6rp8zvsnlj3iytxmeh72ca9bg5o41q"

# for i in range(len(alphabet)):
#     if i % 6 == 0:
#         print()
#     print(alphabet[i], end=" ")

# flag = "herfayo7oqxrz7jwxx15ie20p40u1i"

# print()

# for i in range(len(flag)):
#     if i % 2 == 0:
#         print()
#     print(flag[i], end=" ")


# print("EMPKM7CG51PT96D3OHOENQ9T6KDGQWHL".lower())
# print("EMNRM7CG51PT96D3OHOENQ9T6KDGQWHL".lower())
# print("EMF5M7CG51PT96D3OHOENQ9T6KDGQWHL".lower())
# print("B960M7CGKUPT96D3OHOENQ9T6KDGQWHL".lower())
# print("B9F5M7CGKUPT96D3OHOENQ9T6KDGQWHL".lower())
# print("B9NRM7CGKUPT96D3OHOENQ9T6KDGQWHL".lower())
# print("B9PKM7CGKUPT96D3OHOENQ9T6KDGQWHL".lower())
# print("YHPKM7CG4GPT96D3OHOENQ9T6KDGQWHL".lower())
# print("YHNRM7CG4GPT96D3OHOENQ9T6KDGQWHL".lower())
# print("YHF5M7CG4GPT96D3OHOENQ9T6KDGQWHL".lower())
# print("EM60M7CG51PT96D3OHOENQ9T6KDGQWHL".lower())
# print("I360M7CGCBPT96D3OHOENQ9T6KDGQWHL".lower())
# print("I3F5M7CGCBPT96D3OHOENQ9T6KDGQWHL".lower())
# print("I3NRM7CGCBPT96D3OHOENQ9T6KDGQWHL".lower())
# print("I3PKM7CGCBPT96D3OHOENQ9T6KDGQWHL".lower())
# print("YH60M7CG4GPT96D3OHOENQ9T6KDGQWHL".lower())
# print("EMPK7MGC51TP693DHOEOQNT9K6GDWQLH".lower())
# print("EMNR7MGC51TP693DHOEOQNT9K6GDWQLH".lower())
# print("EMF57MGC51TP693DHOEOQNT9K6GDWQLH".lower())
# print("I3607MGCCBTP693DHOEOQNT9K6GDWQLH".lower())
# print("I3F57MGCCBTP693DHOEOQNT9K6GDWQLH".lower())
# print("I3NR7MGCCBTP693DHOEOQNT9K6GDWQLH".lower())
# print("I3PK7MGCCBTP693DHOEOQNT9K6GDWQLH".lower())
# print("EM607MGC51TP693DHOEOQNT9K6GDWQLH".lower())
# print("B9607MGCKUTP693DHOEOQNT9K6GDWQLH".lower())
# print("B9F57MGCKUTP693DHOEOQNT9K6GDWQLH".lower())
# print("B9NR7MGCKUTP693DHOEOQNT9K6GDWQLH".lower())
# print("B9PK7MGCKUTP693DHOEOQNT9K6GDWQLH".lower())
# print("YHPK7MGC4GTP693DHOEOQNT9K6GDWQLH".lower())
# print("YH607MGC4GTP693DHOEOQNT9K6GDWQLH".lower())
# print("YHF57MGC4GTP693DHOEOQNT9K6GDWQLH".lower())
# print("YHNR7MGC4GTP693DHOEOQNT9K6GDWQLH".lower())

# alphabet for matrix
alphabet = "0fkdwu6rp8zvsnlj3iytxmeh72ca9bg5o41q"

# square size
SQUARE_SIZE = 6


def generate_square(alphabet):
    assert len(alphabet) == pow(SQUARE_SIZE, 2)
    matrix = []
    for i, letter in enumerate(alphabet):
        if i % SQUARE_SIZE == 0:
            row = []
        row.append(letter)
        if i % SQUARE_SIZE == (SQUARE_SIZE - 1):
            matrix.append(row)
    return matrix


def get_index(letter, matrix):
    for row in range(SQUARE_SIZE):
        for col in range(SQUARE_SIZE):
            if matrix[row][col] == letter:
                return (row, col)
    print("letter not found in matrix.")
    exit()


# decrypt each pair
def decrypt_pair(pair, matrix):
    # get the indices in the matrix
    p1 = get_index(pair[0], matrix)
    p2 = get_index(pair[1], matrix)

    # if the first index is the same
    if p1[0] == p2[0]:
        return (
            matrix[p1[0]][(p1[1] - 1) % SQUARE_SIZE]
            + matrix[p2[0]][(p2[1] - 1) % SQUARE_SIZE]
        )

    # if the second index is the same
    if p1[1] == p2[1]:
        return (
            matrix[(p1[0] - 1) % SQUARE_SIZE][p1[1]]
            + matrix[(p2[0] - 1) % SQUARE_SIZE][p2[1]]
        )

    # else
    return matrix[p1[0]][p2[1]] + matrix[p2[0]][p1[1]]


# decrypt string function
def decrypt_string(s, matrix):
    # place to store result
    result = ""

    # Iterate through string two at a time
    for i in range(0, len(s), 2):
        # pass the pairs to the decrypt_pair function
        result += decrypt_pair(s[i : i + 2], matrix)

    # return result
    return result


# generate square
m = generate_square(alphabet)

# encrypted message
enc_msg = "herfayo7oqxrz7jwxx15ie20p40u1i"

# decrypt string
print(decrypt_string(enc_msg, m))
