#include <stdio.h>
#include <inttypes.h>
#include <assert.h>
#include <stdlib.h>

typedef struct
// __attribute__((packed))
{
  uint16_t A : 8;
  uint16_t B : 16;
  uint16_t C : 8;
} Foo;


int main(int argc, char **argv)
{
  Foo *foo = calloc(sizeof(Foo), 1);

  foo->A = -1;
  foo->B = -1;
  foo->C = -1;

  fwrite(foo, sizeof(Foo), 1, stdout);


  // printf("align\t%lu\n", __alignof__(Foo));
  // printf("size\t%lu\n", sizeof(Foo));
  free(foo);
  return 0;
}
