#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void init(){
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    alarm(180);
}

void win(){
    system("cat FLAG");
}

int main(){
    init();
    int answer;
    printf("15+1=0x");
    scanf("%d", &answer);
    if(answer == 10){
        win();
    }
    else{
        puts("incorecct:(");
    }
    return 0;
}