#include <stdio.h>
#include <stdint.h>
#include <string.h>

typedef struct
__attribute__ ((packed))
{
  uint8_t a: 4;
  uint8_t b: 8;
  uint8_t c: 4;
} Foo;

typedef union {
  Foo foo;
  uint8_t x[sizeof(Foo)];
} U;

int main(int argc, char** argv) {
    printf("%lu\n", __alignof__(Foo));
    printf("%lu\n", sizeof(Foo));

    U u;
    memset(&u, 0, sizeof(U));
    u.foo.b = -1;
    // Because we are on a little endian machine, it makes more sense to print
    // the bytes in reverse order.
    // We expect this to print: "0f f0"
    for(int i=sizeof(Foo)-1; i>=0; --i) {
        printf("%02x ", u.x[i]);
    }
    printf("\n");
    return 0;
}
