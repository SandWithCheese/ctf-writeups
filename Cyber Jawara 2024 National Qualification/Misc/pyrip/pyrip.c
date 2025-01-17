#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <sys/user.h>
#include <sys/wait.h>

void trace(pid_t pid) {
  int status;
  struct user_regs_struct regs;

  waitpid(pid, &status, 0);
  ptrace(PTRACE_CONT, pid, 0, 0);

  while (1) {
    ptrace(PTRACE_CONT, pid, 0, 0);
    waitpid(pid, &status, 0);
    if (WSTOPSIG(status) != SIGCHLD) {
      break;
    }
  }

  if (WSTOPSIG(status) == SIGSEGV) {
    printf("Segmentation fault\n");
    printf("RIP: 0x%llx\n", regs.rip);
    ptrace(PTRACE_GETREGS, pid, 0, &regs);
    if (regs.rip == 0xc0ffeedecaf) {
      system("cat flag.txt");
    }
  }

  exit(0);
}

void py_exec() {
  ptrace(PTRACE_TRACEME, 0, 0, 0);
  close(2);
  dup2(1, 2);
  setreuid(65534, 65534);
  setregid(65534, 65534);
  execl("/usr/bin/python3", "/usr/bin/python3", NULL);
}

int main() {
  pid_t pid;

  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  setvbuf(stderr, 0, 2, 0);

  pid = fork();

  if (pid == -1) {
    exit(-1);
  }

  if (pid == 0) {
    py_exec();
  }
  else {
    trace(pid);
  }

  return 0;
}