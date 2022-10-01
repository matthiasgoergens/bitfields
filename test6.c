#include<stdio.h>

typedef struct
// __attribute__((packed))
{
  // unsigned int Ax;
  unsigned short A;
  unsigned short B;
  // unsigned int A;
  unsigned short _;
} Bar;

// typedef union {
//   unsigned long long int x;
//   Bar bar;
// } U;

// Hmm, size is different depending on alignment of largest type?
// sizeof seems to be a multiple of the largest type.

int main(int argc, char** argv) {
    printf("sizeof %lu\n", sizeof(Bar));
    return 0;
}
