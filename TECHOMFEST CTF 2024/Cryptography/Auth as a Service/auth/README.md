# Auth as a Service - User - Kernel

## TL;DR

Auth as a Service - User
- `interface.c` -> `/home/ctf/interface`

Auth as a Kernel
- `char.c` `char.h` `aes.c` `aes.h` -> `/root/auth.ko`

## Structure

```
.
├── Dockerfile
├── README.md
├── bin
│   ├── auth.ko
│   ├── interface
│   ├── ld-linux-x86-64.so.2
│   └── libc.so.6
├── docker-compose.yml
├── qemu
│   ├── bzImage
│   ├── rootfs.cpio.gz
│   └── run.sh
└── src
    ├── Makefile
    ├── aes.c
    ├── aes.h
    ├── char.c
    ├── char.h
    └── interface.c

3 directories, 16 files
```

## Files

- `Dockerfile`, `docker-compose.yml` ~ Config docker images and container to host this challenge
- `bin` ~ Binary of a challenge and mostly important for debugging process
- `qemu` ~ All the challenge files in here
- `src` ~ Source of a challenge

#### `ls bin/`
- `auth.ko` ~ The kernel module (**Kernel**)
- `interface` ~ The auth interface binary (**Service - User**)
- `libc.so.6` ~ The libc for `interface` binary (**User**)
- `ld-linux-x86-64.so.2` ~ The ld for `interface` binary (**User**)

#### `ls qemu/`
- `bzImage` ~ Compressed linux kernel image
- `rootfs.cpio.gz` ~ Initial root filesystem
- `run.sh` ~ Qemu run script

#### `ls src/`
- `Makefile` ~ Build script for kernel and interface
- `aes.c` ~ AES module (**Kernel**)
- `aes.h` ~ Header file `aes.c` (**Kernel**)
- `char.c` ~ Character Device module (**Kernel**)
- `char.h` ~ Header file `char.c` (**Kernel**)
- `interface.c` ~ Auth interface source (**Service - User**)

## Instruction
### Auth as a Service
- It's clear that your scope are not related with exploiting binary itself.
- Your work will be solely focused on `interface.c` without considering the others.
- The AES CBC code in `aes.c` `aes.h` is **not vulnerable**, but the implementation in auth service has vulnerabilities
- There's no fancy AES exploit this time
- All you have to do is to elevate your privilege into admin

### Auth as a User
- Here you have admin on, and have privilege in general as admin user
- `/home/ctf/interface` is a vulnerable binary
- Try to exploiting `/home/ctf/interface` binary to achieve shell
- You may assumed that the AES, Busybox, and Qemu are **not vulnerable**

### Auth as a Kernel
- You have shell on machine and running as user `ctf`
- `/root/auth.ko` is a vulnerable kernel driver
- Try to exploiting `/dev/auth` to achieve privilege escalation as `root`
- You may assumed that the AES, Busybox, and Qemu are **not vulnerable**

## Debug (most likely Auth as a Service)

### Decompress
```bash
$ mkdir rootfs && cd rootfs
$ gzip -d < ../rootfs.cpio.gz | cpio -iv
$ cd ..
```
### Compress
```bash
$ gcc -static -o rootfs/home/ctf/interface ../src/interface.c
$ cd rootfs
$ find . | cpio -H newc -o --owner=root | gzip > ../rootfs.cpio.gz
$ cd ..
```
Because **Auth as a Service** is not fully dependant with the binary, therefore you can debug by compiling the `interface.c` by yourself. You can edit the source as much you want, such as printing variables, inspect memory, and so forth. 

Then, compile with `-static` to make it static binary to avoid error due to inconsistence version of glibc.

**The rest is yours, goodluck**