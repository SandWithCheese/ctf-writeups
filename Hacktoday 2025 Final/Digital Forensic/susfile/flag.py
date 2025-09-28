from pwn import *

host, port = "103.226.138.119", "14045"

conn = remote(host, port)


def answer_question(question_number, answer):
    conn.sendlineafter(b"(Enter question number 1-9): ", question_number)
    conn.sendlineafter(b"Your answer: ", answer)


answer_question(b"1", b".xlsm")

answer_question(b"2", b"certutil.exe, conhost.exe")

answer_question(b"3", b"Agent Tesla")

answer_question(b"4", b"Dell, 2021:08:19 14:03:52Z")

answer_question(b"5", b"56")

answer_question(b"6", b"3; A3,A4,A5")

answer_question(b"7", b"Sheet1, ThisWorkbook, Workbook")

answer_question(b"8", b"52.59.234.180, Germany")

answer_question(b"9", b"certutil.exe, Grfciafhjqghqqtyyb.exe.exe, vbHide")

conn.interactive()
