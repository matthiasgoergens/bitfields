#include<stdio.h>

typedef struct
// __attribute__((packed))
{
  unsigned char _;
  unsigned int A: 1;
} Bar;

// typedef union {
//   unsigned long long int x;
//   Bar bar;
// } U;

int main(int argc, char** argv) {
    printf("sizeof %lu\n", sizeof(Bar));
    return 0;
}
