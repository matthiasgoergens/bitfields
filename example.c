#include<stdio.h>
#include<inttypes.h>



typedef struct
__attribute__ ((ms_struct))
{
    uint8_t A;
    uint16_t B: 1;
} Foo;

int main(int argc, char** argv) {
    printf("%lu\n", __alignof__(Foo));
    printf("%lu\n", sizeof(Foo));
    return 0;
}
