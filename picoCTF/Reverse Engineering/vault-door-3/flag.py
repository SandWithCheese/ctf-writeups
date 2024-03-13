# int i;
#         for (i=0; i<8; i++) {
#             buffer[i] = password.charAt(i);
#         }
#         for (; i<16; i++) {
#             buffer[i] = password.charAt(23-i);
#         }
#         for (; i<32; i+=2) {
#             buffer[i] = password.charAt(46-i);
#         }
#         for (i=31; i>=17; i-=2) {
#             buffer[i] = password.charAt(i);
#         }
#         String s = new String(buffer);
#         return s.equals("jU5t_a_sna_3lpm12g94c_u_4_m7ra41");

buffer = ["" for _ in range(32)]
distorted_flag = "jU5t_a_sna_3lpm12g94c_u_4_m7ra41"

block1 = distorted_flag[:8]
block2 = distorted_flag[8:16][::-1]
rest = distorted_flag[16:]

block3 = ""
for i in range(0, len(rest), 2):
    block3 += rest[i]

block3 = block3[::-1]

block4 = ""
for i in range(1, len(rest), 2):
    block4 += rest[i]

last_block = ""
for i in range(len(block3)):
    last_block += block3[i] + block4[i]

flag = block1 + block2 + last_block
print("picoCTF" + "{" + flag + "}")
