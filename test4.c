#include<stdio.h>

typedef struct
// __attribute__((packed))
{
  unsigned int _;
  unsigned int A: 32;
  unsigned long long int B: 1;
} Bar;

// typedef union {
//   unsigned long long int x;
//   Bar bar;
// } U;

int main(int argc, char** argv) {
    printf("sizeof %lu\n", sizeof(Bar));
    return 0;
}
