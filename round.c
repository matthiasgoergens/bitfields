#include<stdio.h>
#include<inttypes.h>

static inline
int round_down(int numToRound, int multiple)
{
    if (multiple == 0)
        return numToRound;
    return (numToRound / multiple) * multiple;
}

int main(int argc, char** argv) {
    printf("%i\n", round_down(-4, 8));
    return 0;
}
