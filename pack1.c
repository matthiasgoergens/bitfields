#include<stdio.h>
#include<inttypes.h>

// #pragma ms_struct on
#pragma pack(1)

typedef struct
__attribute__ ((ms_struct))
{
    uint8_t A: 3;
    uint8_t B: 6;
    uint8_t C: 3;
} Foo;

typedef union {
  unsigned long long int x;
  Foo foo;
} U;


int main(int argc, char** argv) {
    printf("%lu\n", __alignof__(Foo));
    printf("%lu\n", sizeof(Foo));
    
    U u;
    u.x = 0;
    printf("u.x:\t%llb\n", u.x);
    // u.foo.A = 0b111;
    u.foo.B = -1;
    printf("u.x:\t%llb\n", u.x);
    printf("B:\t%b\n", u.foo.B);
    return 0;
}

// 1 11111000
