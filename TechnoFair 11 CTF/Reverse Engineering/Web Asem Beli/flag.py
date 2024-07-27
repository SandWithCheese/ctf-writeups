def extract_flag():
    # Create a dictionary representing the structure `c`
    c = {
        'a': 84, 'b': 101, 'c': 99, 'd': 104, 'e': 110, 'f': 111, 'g': 70, 'h': 97,
        'i': 105, 'j': 114, 'k': 49, 'l': 49, 'm': 123, 'n': 76, 'o': 48, 'p': 104,
        'q': 95, 'r': 107, 's': 79, 't': 107, 'u': 95, 'v': 57, 'w': 73, 'x': 116,
        'y': 85, 'z': 125, 'aa': 0
    }

    # Convert the dictionary to a list of characters
    flag = ''.join(chr(c[key]) for key in c if key != 'aa')
    
    return flag

flag = extract_flag()
print(flag)
