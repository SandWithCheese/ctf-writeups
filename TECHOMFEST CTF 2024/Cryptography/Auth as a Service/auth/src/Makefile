obj-m := auth.o
auth-objs := char.o aes.o

all: interface
	make -C ../../linux-6.6-rc5 M=$(PWD) modules

clean:
	make -C ../../linux-6.6-rc5 M=$(PWD) clean

interface:
	gcc -o interface interface.c -no-pie -fno-stack-protector
