#include<stdio.h>
#include<inttypes.h>

typedef struct {
  // uint8_t _;
  unsigned int a: 12;
  unsigned int b: 8;
  unsigned int c: 8;
} Foo;

// typedef union {
//   Foo foo;
//   unsigned int x;
// } U;

typedef union {
  Foo foo;
  char x[sizeof(Foo)];
} Uu;

int main(int argc, char** argv) {
  printf("align\t%lu\n", __alignof__(Foo));
  printf("size\t%lu\n", sizeof(Foo));
  // U u;
  // u.x = 0;
  // u.foo.a = 0xab;
  // u.foo.b = 0xcd;
  // u.foo.c = 0xef;
  // printf("%x\n", u.x);
  // printf("%x\n", u.foo.a);

  Uu uu;
  for(int i=0; i<sizeof(Foo); ++i) {
    uu.x[i] = 0;
  }
  uu.foo.a = 0xab;
  uu.foo.b = 0xcd;
  uu.foo.c = 0xef;
  for(int i=0; i<sizeof(Foo); ++i) {
    uint8_t y = uu.x[i];
    printf("%02x ", y);
  }
  printf("\n");
  printf("%x %x %x\n", uu.foo.a, uu.foo.b, uu.foo.c);
  uint64_t f = *((uint64_t*) &uu.foo);
  printf("%016llx\n", f);

  return 0;
}
