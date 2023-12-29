section .text:
global _start
_start:
    lea edx, s    
    mov di, edx   
    lea bh, flag   
    mov bl, bh 
    mov cl, 25h
    add bl, cl  

    L1 : 
        add di, 1  
        mov al, [edx]    
        xchg [bh], al   
        mov ch, [di]       
        xchg [bl], ch    
        dec bl
        add edx, 2
        inc bh
        cmp edx, cl
        jl L1
        ret
section .data:
s db 's', '}', 'l', 'h', 'a', 'u', 's', 'p', 'h', '3', 'r', '5', 'o', '_', 'o', 'h', 't', 'u', '7', 'p', '{', '_', 'p', 'u', '3', 'l', 'm', 'u', '4', 'd', 'n', '_', '4', 'n', 's', '4' 
flag db ''