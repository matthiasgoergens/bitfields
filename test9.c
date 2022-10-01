#include<stdio.h>
#include<inttypes.h>

typedef struct
{
  uint8_t A: 1;
} Foo;

// typedef union {
//   unsigned long long int x;
//   Bar bar;
// } U;

// Hmm, size is different depending on alignment of largest type?
// sizeof seems to be a multiple of the largest type.

int main(int argc, char** argv) {
    printf("__alignof__ %lu\n", __alignof__(Foo));
    printf("sizeof %lu\n", sizeof(Foo));
    return 0;
}
