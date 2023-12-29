from string import printable
import requests

# function checkValidity(password){
#     const arr = Array.from(password).map(ok);
#     function ok(e){
#         if (e.charCodeAt(0)<= 122 && e.charCodeAt(0) >=97 ){
#         return e.charCodeAt(0);
#     }}

#     let sum = 0;
#     for (let i = 0; i < arr.length; i+=6){
#         var add = arr[i] & arr[i + 2];
#         var or = arr[i + 1] | arr[i + 4];
#         var xor = arr[i + 3] ^ arr[i + 5];
#         if (add === 96   && or === 97   && xor === 6) sum += add + or - xor;
#     }
#    return  sum === 187 ? !0 : !1;
# }

# arr[0] & arr[2] = 96
# arr[1] | arr[4] = 97
# arr[3] ^ arr[5] = 6


possible_and = []
for i in printable:
    for j in printable:
        if ord(i) & ord(j) == 96 and (97 <= ord(i) <= 122) and (97 <= ord(j) <= 122):
            possible_and.append([i, j])
            break


possible_or = []
for i in printable:
    for j in printable:
        if ord(i) | ord(j) == 97 and (97 <= ord(i) <= 122) and (97 <= ord(j) <= 122):
            possible_or.append([i, j])
            break

possible_xor = []
for i in printable:
    for j in printable:
        if ord(i) ^ ord(j) == 6 and (97 <= ord(i) <= 122) and (97 <= ord(j) <= 122):
            possible_xor.append([i, j])
            break

print(len(possible_and))
print(possible_or)
print(len(possible_xor))

s = requests.Session()
for pair_and in possible_and:
    for pair_xor in possible_xor:
        password = pair_and[0] + "a" + pair_and[1] + pair_xor[0] + "a" + pair_xor[1]
        print(f"[*] Trying {password}")
        res = s.post(
            url="http://chal.pctf.competitivecyber.club:9096/check.php",
            data={"password": password},
        ).text

        if "incorrect" not in res:
            print(res)
            quit()
        # print(password)
