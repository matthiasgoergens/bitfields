#include<stdio.h>
#include<inttypes.h>

typedef struct
{{
  uint32_t A: 1;
  uint64_t B: 1;
}} Foo;

int main(int argc, char** argv) {{
    printf("%lu\n", __alignof__(Foo));
    printf("%lu\n", sizeof(Foo));
    return 0;
}}
