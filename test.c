#include<stdio.h>

typedef struct {
  int a: 1;
} Foo;

int main(int argc, char** argv) {
  Foo foo;
  foo.a = 1;
  printf("%i\n", foo.a);
  return 0;
}
