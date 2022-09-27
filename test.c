#include<stdio.h>

struct Foo {
  unsigned int A: 1;
  unsigned short B: 16;
};

struct Bar {
  unsigned long long int A: 1;
  unsigned int B: 32;
};

int main(int argc, char** argv) {
    struct Foo foo;
    foo.A = 0;
    foo.B = 1;
    printf("%d %d\n", foo.A, foo.B);


    struct Bar bar;
    bar.A = 0;
    bar.B = 1;
    printf("%d %d\n", bar.A, bar.B);
    return 0;
}
