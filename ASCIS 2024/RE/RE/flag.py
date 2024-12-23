from pwn import *

local_38 = "1317111e3438292d"
local_30 = "1150162c1c161911"
local_28 = "404423f3a1f4717"
local_20 = "181a513b1a302d"
uStack_19 = "18442d54"
local_45 = "657379656b"
uStack_40 = "657263"
uStack_3d = "79656b74"

enc = (
    # uStack_3d
    # + uStack_40
    # + local_45
    # + uStack_19
    local_20
    + local_28
    + local_30
    + local_38
)

flag = ""
for i in range(0, len(enc), 2):
    block = enc[i : i + 2]
    # print(chr(int(block, 16)), end="")
    flag += chr(int(block, 16))

print(flag)

#   for (local_1c = 0; local_1c < param_3; local_1c = local_1c + 1) {
#     bVar1 = *(byte *)(param_1 + local_1c);
#     uVar2 = FUN_001053f9(param_2);
#     *(byte *)(param_1 + local_1c) = bVar1 ^ *(byte *)(param_2 + (ulong)(long)local_1c % uVar2);
#   }

# xored_val = ""
# for i in range(0, 70, 2):
#     block1 = ord(enc[i : i + 2])

print(len(enc))
