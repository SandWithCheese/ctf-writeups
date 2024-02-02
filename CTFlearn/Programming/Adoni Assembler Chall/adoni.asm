; This is a comment
; CTFlearn Assembly Programming Challenge "Adoni" by kcbowhunter

section .data
    welcome db "Hello CTFlearn Adoni Assembler Challenge!",0x0a
    noflag db "Sorry no flag for you :-(",0x0a
    adoni db 67, 84, 70, 108, 101, 97, 114, 110, 123, 75, 117, 114, 110, 48, 48, 108, 95, 68, 105, 115, 116, 114, 105, 99, 116, 125, 0x0a
    congrats db 67, 111, 110, 103, 114, 97, 116, 115, 44, 32, 121, 111, 117, 32, 102, 111, 117, 110, 100, 32, 116, 104, 101, 32, 102, 108, 97, 103, 33, 0x0a

section .text
    global _start

_start:
    mov rax, 1      ; sys_write system call
    mov rdi, 1      ; stdout (write to screen)
    mov rsi, welcome   ; memory location of string to write
    mov rdx, 42     ; number of characters in string to write
    syscall

    mov rax, 1      ; sys_write system call
    mov rdi, 1      ; stdout
    mov rsi, noflag ; memory location of string to write
    mov rdx, 26     ; number of characters in string to write
    syscall

    mov rax, 60     ; exit system call
    mov rdi, 0
    syscall

;   this is the assembly code to print the flag
_printflag:
    mov rax, 1      ; sys_write system call
    mov rdi, 1
    mov rsi, congrats
    mov rdx, 30
    syscall

    mov rax, 1      ; sys_write system call
    mov rdi, 1
    mov rsi, adoni
    mov rdx, 27
    syscall

    mov rax, 60     ; exit system call
    mov rdi, 0
    syscall



