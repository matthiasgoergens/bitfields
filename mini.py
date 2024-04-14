import ctypes
from ctypes import Structure, c_uint, c_ulonglong

# class Foo(Structure):
#     _fields_ = [("A", c_uint, 1), ("B", c_ushort, 16)]


class Bar(Structure):
    # _fields_ = [("A", c_ulonglong, 20), ("B", c_uint, 24), ("C", c_ulonglong, 8)]
    # _fields_ = [("A", c_ulonglong, 20), ("B", c_ulonglong, 24), ("C", c_ulonglong, 8)]
    _fields_ = [("A", c_ulonglong, 20), ("B", c_uint, 24)]
    # _fields_ = [("A", c_uint, 20), ("B", c_uint, 24), ("C", c_uint, 8)]
    # _fields_ = [("A", c_uint, 20), ("B", c_uint, 24), ("C", c_ulonglong, 8)]
    # _fields_ = [("A", c_ulonglong, 10), ("B", c_uint, 8), ("C", c_uint, 8)]
    # _fields_ = [("A", c_uint, 8), ("B", c_uint, 8), ("C", c_uint, 8), ("D", c_uint, 8)]


def test():
    # for a in [Foo(), Bar()]:
    for a in [Bar()]:
        a.A = -1
        a.B = -1
        a.A = 0x12345
        a.B = 0x6789AB
        # a.C = 0xcd
        # a.D = 0xbb
        print(f"sizeof: {ctypes.sizeof(a)}")
        print(hex(a.A), hex(a.B))
        # print(hex(a.C))
        # print(hex(a.A), hex(a.B), hex(a.C))


0xCC00BBBBFFF0AAAA  # gcc / clang
0xBBBCC0000000AAAA  # python
0xBBB000000000AAAA  # without c

0xCD_6789AB_FFF_12345  # gcc / clang
0xCD_6789AB_000_12345  # all ints in python
0x9AB_CD_000000_12345  # python


#   v 52 bits offset
0x9AB_0_0000000_12345  # without c

# 8ULL, 8U in C
0xFFFFFFFFFFFF_AB_45  # gcc / clang
0x0000_0000_FFFFFF_FF
#       v 40 bits offset. = 32 + 8
0x0000_AB00_000000_45  # python

# x=      0xffffffff
# 0x0000ab4500000000 # 8U 8U
# 0xffffffffffffab45

0x000000000002AF4500000000
0xFFFFFFFFFC02AF45
0xFFFFFFFFFFF2AF45

# (*pbitofs + bitsize + 7) & ~(8 * dict->align - 1);

0o3777777740003777777
0o3777777, 0o77777777
0o3777777, 0o77777777


def test_round():
    bitofs = 20
    bitsize = 1
    dict_align = 2
    x = (bitofs + bitsize + 7) & ~(8 * dict_align - 1)
    print(x)


if __name__ == "__main__":
    test()
