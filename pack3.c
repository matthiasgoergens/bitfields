#include<stdio.h>
#include<inttypes.h>

// #pragma pack(1)

typedef struct
// __attribute__ ((ms_struct))
{
    uint8_t A;
    uint16_t B: 8;
} Foo;

int main(int argc, char** argv) {
    printf("%lu\n", __alignof__(Foo));
    printf("%lu\n", sizeof(Foo));
    return 0;
}
