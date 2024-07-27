# Step 1: Start with the original encrypted string
encrypted_string = "16_10_13_x_6t_4_1o_9_1j_7_9_1j_1o_3_6_c_1o_6r"

# Step 2: Split the string by underscores and convert from base-36
parts = encrypted_string.split("_")
numbers = [int(part, 36) + 10 for part in parts]
chars = [chr(num) for num in numbers]

# Step 3: Combine characters into a single string
combined = "".join(chars)

# Step 4: Apply XOR with 123
xor_chars = [chr(123 ^ ord(c)) for c in combined]
xor_string = "".join(xor_chars)

# Step 5: Shift characters back by -12 and +3
shifted_back_12 = [chr(ord(c) - 12) for c in xor_string]
shifted_back_12_string = "".join(shifted_back_12)

shifted_back_3 = [chr(ord(c) + 3) for c in shifted_back_12_string]
original_string = "".join(shifted_back_3)

print(f"The original flag is: {original_string}")
