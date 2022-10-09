#include <stdio.h>
#include <inttypes.h>
#include <assert.h>
#include <string.h>

typedef struct
// __attribute__((packed))
{
  uint16_t A : 8;
  uint16_t B : 16;
  uint16_t C : 8;
} Foo;

typedef union {
  Foo foo;
  char x[sizeof(Foo)];
} Uu;

// Hmm, size is different depending on alignment of largest type?
// sizeof seems to be a multiple of the largest type.

int main(int argc, char **argv)
{
  assert(sizeof(Foo)==sizeof(Uu));
  Uu u;
  memset_explicit(&u, 0, sizeof(u));

  u.foo.A = -1;
  u.foo.B = -1;
  u.foo.C = -1;

  {
    FILE *file = fopen("output", "wb");
    if (file != NULL)
    {
      fwrite(&u.foo, sizeof(Foo), 1, file);
      fclose(file);
    }
  }

  {
    Foo b2;
    FILE *file = fopen("output", "rb");
    if (file != NULL)
    {
      fread(&b2, sizeof(Foo), 1, file);
      fclose(file);
    }
  }

  printf("align\t%lu\n", __alignof__(Foo));
  printf("size\t%lu\n", sizeof(Foo));
  return 0;
}
