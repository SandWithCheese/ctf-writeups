#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdint.h>
#include <sys/ioctl.h>
#include <string.h>
#include <regex.h>
#include <sys/mman.h>
#include <sys/prctl.h>

#define MAX_SIZE 0x100
#define BLOCKSIZE 0x10
#define SET_KEY 0xAE5CBC1
#define SET_IV  0xAE5CBC2

int fd;
char *admin_flag;

struct secret_t {
    uint8_t key[16];
    uint8_t iv[16];
} secret;

void err(const char *msg){
    puts(msg);
    exit(1);
}

ssize_t input(const char *msg, uint8_t *ptr, int len){
    printf("%s", msg);
    ssize_t recv = 0;
    while(recv < len){
        if(read(0, &ptr[recv], 1) < 0) exit(1);
        if(ptr[recv] == '\n'){
            ptr[recv] = '\0';
            break;
        } recv++;
    } return recv;
}

ssize_t hxput(const char *msg, uint8_t *ptr, int len){
    char *buf = malloc(len * 2);
    ssize_t recv = input(msg, buf, len * 2);
    for (int i = 0; i < recv - 1; i += 2){
        if(sscanf(&buf[i], "%02hhx", &ptr[i/2]) <= 0) exit(-1);
    }
    free(buf);
    return recv / 2;
}

int parse_json_value(char *json, char *username, int *is_admin) {
    regex_t regex;
    regmatch_t match[3];
    size_t len;
    char *tmp;

    if (regcomp(&regex, "\\{\"username\": \"([^\"]*)\", \"admin\": ([^\"]*)\\}", REG_EXTENDED)) return -1;
    if (regexec(&regex, json, 3, match, 0)) return -1;
    
	len = match[1].rm_eo - match[1].rm_so;
    tmp = malloc(len + 1);
    memcpy(tmp, &json[match[1].rm_so], len);

    for (size_t i = 0, j = 0; i < len; i++){
        if((tmp[i] >= '0' && tmp[i] <= '9') || (tmp[i] >= 'A' && tmp[i] <= 'Z') || (tmp[i] >= 'a' && tmp[i] <= 'z') || tmp[i] == '_')
            username[j++] = tmp[i];
	    else break;
    }

    len = match[2].rm_eo - match[2].rm_so;
    *is_admin = (!strncmp(&json[match[2].rm_so], "true", len)) ? 1 : 0;

    free(tmp);
    regfree(&regex);
    return 0;
}

void urandom(uint8_t *ptr, size_t len){
    int fd;
    if((fd = open("/dev/urandom", O_RDONLY)) < 0) exit(-1);
    if(read(fd, ptr, len) != len) exit(-1);
    close(fd);
}

void dashboard(uint8_t **data, int index, int is_admin){
    for(;;){
        printf("\n[[ dashboard ]]\n"
                "1. view user\n"
                "2. flag\n"
                "0. logout\n"
                "D> ");
        int choice, idx;
        char user[64] = { 0 };

        if(scanf("%d%*c", &choice) != 1) exit(1);
        switch (choice) {
        case 1:
            if(is_admin){
                printf("index: ");
                if(scanf("%d%*c", &idx) < 1) exit(1);

                if(idx >= 15){
                    puts("[!] index out of range");
                    break;
                }
                if(!(data[idx + 1][0])){
                    puts("[!] user not found");
                    break;
                }
                printf("creds: %s\n", data[idx + 1]);
                
            } else puts("[!] permission denied");
            break;
        
        case 2:
            if(is_admin) printf("well deserved: %s\n", admin_flag);
            else puts("[!] permission denied");
            break;
        
        case 0: return;

        default:
            if (is_admin) memcpy(user, data[index], MAX_SIZE);
            puts("[!] invalid choice");
            break;
        }
    }
}

void signup(uint8_t **data, int index){

    char cookie[MAX_SIZE] = { 0 };
    char username[64] = { 0 };
    size_t len;

    if(index >= 16){
        puts("[!] too much user");
        return;
    }

    urandom(secret.iv, BLOCKSIZE);
    ioctl(fd, SET_IV, secret.iv);

    if(!(len = input("username << ", username, 64)) || len > 64-1)
        err("[-] username length error");

    len = sprintf(cookie, "{\"username\": \"%s\", \"admin\": %s}", username, "false");

    pwrite(fd, cookie, len, index * MAX_SIZE);

    printf("cookie   >> ");
    for(size_t i = 0; i < (len + BLOCKSIZE - (len % BLOCKSIZE)); i++){
        printf("%02hhx", data[index][i]);
    } putchar('\n');
}

void signin(uint8_t **data, int index){
    
    char cookie[MAX_SIZE] = { 0 };
    char username[64] = { 0 }, umatched[64] = { 0 };
    int is_admin = 0;
    size_t len;
    
    if(!index){
        puts("[!] sign up first");
        return;
    }
    if(!(len = input("username << ", username, 64)) || len > 64-1)
        err("[-] username length error");
    
    if(!(len = hxput("cookie   << ", cookie, MAX_SIZE)) || len > MAX_SIZE)
        err("[-] cookie length error");
    
        if(pread(fd, cookie, len, index * MAX_SIZE) < 0)
            err("[-] cookie invalid");
    
        if(!parse_json_value(cookie, umatched, &is_admin)){
            if(!strcmp(username, umatched)) dashboard(data, index, is_admin);
            else goto reset;
        } else goto reset;
    
    return;

reset:
    memset(data[index], 0, MAX_SIZE);
    puts("[!] sign in failed");
    return;
}

int main(int argc, char*argv[]){
    int idx = 1;
    uint8_t **data;

    if((fd = open("/dev/auth", O_RDWR)) < 0) err("error: open failed");
    if((data = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0)) == MAP_FAILED) err("error: mmap failed");

    urandom(secret.key, BLOCKSIZE);
    ioctl(fd, SET_KEY, secret.key);

    data[0] = (uint8_t*)&secret;
    for (int i = 1; i < 16; i++)
        data[i] = (uint8_t*)data + MAX_SIZE * i;

    admin_flag = argv[1];

    for(;;){
        printf("\n(( menu ))\n"
                "1. sign up\n"
                "2. sign in\n"
                "0. exit\n"
                "M> ");
        int choice;
        if(scanf("%d%*c", &choice) != 1) exit(1);

        switch (choice) {
        case 1: signup(data, idx); idx++; break;
        case 2: signin(data, idx - 1); break;
        case 0: puts("Bye"); exit(0);
        default: break;
        }
    }
}

__attribute__((constructor))
void setup(void){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}
