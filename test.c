#include<stdio.h>

struct Foo {
  unsigned int A: 1;
  unsigned short B: 16;
};

typedef struct
// __attribute__((packed))
{
  unsigned long long int A: 20;
  // // unsigned int A: 8;
  // // unsigned int A: 20;
  // // unsigned int A: 8;
  // // unsigned long long int B: 24;
  // unsigned char B: 6;
  unsigned int B: 24;
  // // unsigned long long int C: 8;
  // unsigned int C: 8;
} Bar;

typedef union {
  unsigned long long int x;
  Bar bar;
} U;

int main(int argc, char** argv) {
    // struct Foo foo;
    // foo.A = 0;
    // foo.B = 1;
    // printf("%d %d\n", foo.A, foo.B);
    // printf("sizeof %lu\n", sizeof(foo));


    U u;

    u.x = 0;
    printf("%llx\n", u.x);


    u.bar.A = -1; // 0x12345;
    u.bar.B = -1; // 0x6789ab;
    // u.bar.C = 0;
    printf("%llo\n", u.x);

    // printf("%x %x %x\n", u.bar.A, u.bar.B, u.bar.C);
    printf("%o %o\n", u.bar.A, u.bar.B);
    // u.bar.A = -1;
    // u.bar.B = -1;

    // printf("%x %x\n", u.bar.A, u.bar.B);
    // printf("%llx\n", u.x);

    

    printf("sizeof %lu\n", sizeof(Bar));
    return 0;
}
