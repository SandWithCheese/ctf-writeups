all: only_admin

only_admin: only_admin.c
	gcc -Wl,-z,relro,-z,now -o $@ $<

clean:
	rm only_admin
