import hashlib

key_part_static1_trial = "picoCTF{1n_7h3_|<3y_of_"
key_part_dynamic1_trial = ""
key_part_static2_trial = "}"


bUsername_trial = b"PRITCHARD"
positions = [4, 5, 3, 6, 2, 7, 1, 8]

for position in positions:
    key_part_dynamic1_trial += hashlib.sha256(bUsername_trial).hexdigest()[position]

flag = key_part_static1_trial + key_part_dynamic1_trial + key_part_static2_trial
print(flag)
