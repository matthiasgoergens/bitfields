#include<stdio.h>
#include<inttypes.h>
#include <stdlib.h>



typedef struct

{

} Foo;

int main(int argc, char** argv) {
    Foo *foo = calloc(sizeof(Foo), 1);
    
    fwrite(foo, sizeof(Foo), 1, stdout);
    fflush(stdout);
    free(foo);
    return 0;
}
