
#include<stdio.h>
#include<inttypes.h>
#include <stdlib.h>

#pragma pack(1)

typedef struct
__attribute__ ((ms_struct))
{
    int64_t XOHSRXZLEQAHZLXFWV: 31;
    int16_t XPP: 15;
    int32_t RTWWDTXXJIQXI;
    uint8_t VNDYVIGBN;
    uint16_t ZH: 16;
    uint16_t XHVXIR: 1;
    uint64_t LNZZJGIURGAO;
    uint16_t TQT: 11;
    int32_t GO;
} Foo;

int main(int argc, char** argv) {
    Foo *foo = calloc(sizeof(Foo), 1);
    foo->XOHSRXZLEQAHZLXFWV = -224;
foo->XPP = -7960;
foo->RTWWDTXXJIQXI = -17682;
foo->VNDYVIGBN = -48243;
foo->ZH = -14395;
foo->XHVXIR = 181;
foo->LNZZJGIURGAO = 22855;
foo->TQT = -64886;
foo->GO = -8301909056879711504;
    fwrite(foo, sizeof(Foo), 1, stdout);
    fflush(stdout);
    free(foo);
    return 0;
}

