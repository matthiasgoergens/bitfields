#include<stdio.h>
#include<inttypes.h>

typedef struct
__attribute__((packed))
{
  // unsigned int Ax;
  uint16_t A: 8;
  uint16_t B: 16;
  // uint32_t B: 32;
  uint16_t C: 8;
  // unsigned int A;
  // unsigned short _;
} Bar;

// typedef union {
//   unsigned long long int x;
//   Bar bar;
// } U;

// Hmm, size is different depending on alignment of largest type?
// sizeof seems to be a multiple of the largest type.

int main(int argc, char** argv) {
    Bar b;
    b.A = argc;
    b.B = argc+1;
    b.C = argc+2;
    printf("sizeof %lu\n", sizeof(Bar));
    return 0;
}
