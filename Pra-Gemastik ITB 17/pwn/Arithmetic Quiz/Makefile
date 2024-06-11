all: arithmetic_quiz

arithmetic_quiz: arithmetic_quiz.c
	gcc -Wl,-z,relro,-z,now -o $@ $<
	pwninit --no-template --libc lib/libc.so.6 --ld lib/ld-linux-x86-64.so.2 --bin arithmetic_quiz
	mv arithmetic_quiz_patched arithmetic_quiz

clean:
	rm arithmetic_quiz
