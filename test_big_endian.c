#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

// #define ATTR __attribute__((scalar_storage_order("big-endian")))
// #define ATTR
// #define ATTR __attribute__((scalar_storage_order("little-endian")))

typedef struct __attribute__((scalar_storage_order("little-endian"))) {
    // uint32_t a:32;
    uint32_t a;
    uint32_t b:4;
    uint64_t c:4;
    uint64_t d:12;
} Foo;

typedef union __attribute__((scalar_storage_order("little-endian"))) {
    Foo foo;
    uint8_t x[sizeof(Foo)];
} U;

typedef struct __attribute__((scalar_storage_order("big-endian"))) {
    // uint32_t a:32;
    uint32_t a;
    uint32_t b:4;
    uint64_t c:4;
    uint64_t d:12;
} Bar;

typedef union __attribute__((scalar_storage_order("big-endian"))) {
    Bar bar;
    uint8_t x[sizeof(Bar)];
} V;

int main(int argc, char** argv) {
    // Foo foo = {.a = 0xaabb, .b = 0xff0000aa, .c = 0xabcdefaabbccddee};
    // U u = {.foo.a = 0xaabb, .foo.b = 0xff0000aa, .foo.c = 0xabcdefaabbccddee};
    U u;
    memset(&u, 0, sizeof(U));
    V v;
    memset(&v, 0, sizeof(V));
    
    u = (U) {.foo.a = 0x3456789a, .foo.b = 0xb, .foo.c = 0xc, .foo.d=0xdef};
    v = (V) {.bar.a = 0x3456789a, .bar.b = 0xb, .bar.c = 0xc, .bar.d=0xdef};
    // U v = {.foo = {.a = 0xaabb, .b = 0xff0000aa, .c = 0xabcdefaabbccddee}};

// little-endian struct:
// forward:        a9 bc fe d0 00 00 00 00 // nibbles are backward
// backward:       00 00 00 00 0d ef cb 9a 

// big-endian struct:
// forward:        a9 cb ed 0f 00 00 00 00 // nibbles are backward
// backward:       00 00 00 00 f0 de bc 9a 

// forward:        9a bc de f0 00 00 00 00 // nibbles are forward
// backward:       00 00 00 00 f0 de bc 9a 

    // FILE *f = fopen("out.bin", "wb");
    // size_t written = fwrite(&u, sizeof(Foo), 1, stdout);
    printf("forward u l:\t");
    for(int i=0; i<sizeof(Foo); ++i) {
        // printf("%08b ", u.x[i]);
        printf("%02x ", u.x[i]);
        // printf("%01x", u.x[i] & 0xf);
        // printf("%01x ", u.x[i] >> 4);
    }
    printf("\n");
    
    printf("forward v b:\t");
    for(int i=0; i<sizeof(Bar); ++i) {
        // printf("%08b ", u.x[i]);
        printf("%02x ", v.x[i]);
        // printf("%01x", u.x[i] & 0xf);
        // printf("%01x ", u.x[i] >> 4);
    }
    printf("\n");

    printf("backward u l:\t");
    for(int i=sizeof(Foo)-1; i>=0; --i) {
        printf("%02x ", u.x[i]);
        // printf("%01x", u.x[i] & 0xf);
        // printf("%01x ", u.x[i] >> 4);
    }
    printf("\n");
        printf("backward v b:\t");
    for(int i=sizeof(Bar)-1; i>=0; --i) {
        printf("%02x ", v.x[i]);
        // printf("%01x", u.x[i] & 0xf);
        // printf("%01x ", u.x[i] >> 4);
    }
    printf("\n\n");
    fflush(stdout);
}
