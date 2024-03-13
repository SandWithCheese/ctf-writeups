flag = "COMPFEST15{FLAG}"

test = list(flag)
holder1 = []
for y, x in enumerate(test):
    if not y:
        holder1.append(ord(x) + 1)
    else:
        holder1.append((ord(x) + holder1[y - 1]) % 33554432)

# print(holder1)

holder2 = []
for i, e in enumerate(holder1):
    if not i:
        holder2.append(holder1[i])
    else:
        holder2.append((e + holder1[i - 1]) % 131072)

# print(holder2)

enc = holder1 + holder2
for i, e in enumerate(enc):
    enc[i] = chr(e)

# print("".join(enc))


enc_flag = "DàİŶƻȎɢʓˈ̓͸ϚлѯҧӝՀո֩؍قٶگܒݴޭߣࠗࡼࢰऒॆॻমৢੈભଐୄ୵ப௟ు౳೔ആഺ൬ිชฺຝ໔༈ཫྡဃံၧႝᄃᄹᅱᆤሊቁእዖገጽ᎟᐀ᐳᑩᓦD×ųȐʦ̱ωѰӵ՛؋ڻݒࠕࢪख঄ਝસଡஶ౏ಸഥශຆ༡ྐ࿺႓ᄬᇂቘ዁ጩ᎐ᐪᓵᖽᙔᚹᜟញᠠᢴ᥇᧚ᩀ᪦ᬾᯜ᱄᳗ᵱᷜṳἌᾤ‹₝℄↠∼⊪⌕⎮⑋ⓦ╻◞♅⛜➟⠳⢜⥏"

# 1st step
dec = []
for i, e in enumerate(enc_flag):
    dec.append(ord(e))

# print(dec)

new_holder1 = dec[: len(dec) // 2]
new_holder2 = dec[len(dec) // 2 :]

# print(new_holder1)
# print(new_holder2)

# 2nd step
flag = ""
for y, x in enumerate(new_holder1):
    if not y:
        flag += chr(x - 1)
    else:
        flag += chr(x - new_holder1[y - 1])

print(flag)
