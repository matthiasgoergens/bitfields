#include <stdio.h>
#include <stdint.h>

typedef struct __attribute__((packed, scalar_storage_order("big-endian"))) {
    uint16_t a;
    uint32_t b;
    uint64_t c;
} Foo;

typedef union {
    Foo foo;
    uint8_t x[sizeof(Foo)];
} U;

int main(int argc, char** argv) {
    // Foo foo = {.a = 0xaabb, .b = 0xff0000aa, .c = 0xabcdefaabbccddee};
    U u = {.foo.a = 0xaabb, .foo.b = 0xff0000aa, .foo.c = 0xabcdefaabbccddee};
    U v = {.foo = {.a = 0xaabb, .b = 0xff0000aa, .c = 0xabcdefaabbccddee}};

    FILE *f = fopen("out.bin", "wb");
    size_t written = fwrite(&u, sizeof(Foo), 1, f);
    fclose(f);
}
