#include <stdio.h>
#include <stdlib.h>

// // gcc main.c -no-pie -o lemfao

void init() {
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}

char lemfao[0x150];

void main(int argc, char* argv[]) {
    init();
    printf("free stuff: %#lx\n", &malloc);

    printf("lemfao? ");
    fgets(lemfao, 0x150, stdin);
    
    unsigned long where;
    for(int i = 0; i < 2; i++) {
        printf("hm...? ");
        scanf("%lu", &where);

        printf("huh... ");
        scanf("%lu", where);
    }

    puts("lemfao haha...");
    exit(0);
}