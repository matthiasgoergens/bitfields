from ctypes import Structure, c_uint, c_ulonglong, c_ushort
import ctypes


# class Foo(Structure):
#     _fields_ = [("A", c_uint, 1), ("B", c_ushort, 16)]


class Bar(Structure):
    _fields_ = [
        ("_", c_uint, 32),
        ("A", c_uint, 20),
        ("B", c_ulonglong, 24),
        # ("C", c_ulonglong, 8)
        ]

def test():
    # for a in [Foo(), Bar()]:
    for a in [Bar()]:
        a.A = -1
        a.B = -1
        a.A = 0x12345
        a.B = 0x6789ab
        # a.C = 0xcd
        # a.D = 0xbb
        print(f"sizeof: {ctypes.sizeof(a)} {ctypes.sizeof(Bar)}")
        print(hex(a.A), hex(a.B))
        # print(hex(a.C))
        # print(hex(a.A), hex(a.B), hex(a.C))

0xcc00bbbbfff0aaaa # gcc / clang
0xbbbcc0000000aaaa # python
0xbbb000000000aaaa # without c

0xcd_6789ab_fff_12345 # gcc / clang
0xcd_6789ab_000_12345 # all ints in python
0x9ab_cd_000000_12345 # python


#   v 52 bits offset
0x9ab_0_0000000_12345 # without c

# 8ULL, 8U in C
0xffffffffffff_ab_45 # gcc / clang
0x0000_0000_ffffff_ff
#       v 40 bits offset. = 32 + 8
0x0000_ab00_000000_45 # python

# x=      0xffffffff
# 0x0000ab4500000000 # 8U 8U
# 0xffffffffffffab45

0x000000000002af4500000000
0xfffffffffc02af45
0xfffffffffff2af45

# (*pbitofs + bitsize + 7) & ~(8 * dict->align - 1);

0o3777777740003777777
0o3777777,0o77777777
0o3777777,0o77777777

def test_round():
    bitofs = 20
    bitsize = 1
    dict_align = 2
    x = (bitofs + bitsize + 7) & ~(8 * dict_align - 1)
    print(x)

if __name__ == "__main__":
    test()
