from ctypes import Structure, c_uint, c_ulonglong, c_ushort, c_uint8
from ctypes import sizeof, alignment
import ctypes


class Foo(Structure):
    _fields_ = [
        ("B", c_uint, 1),
        ("C", c_ulonglong, 1)
        ]

# class Bar(Structure):
#     _fields_ = [
#         ("A", c_uint),
#         ("C", c_ushort),
#         ]

def test():
    print(sizeof(Foo))
    print(f"alignment: {alignment(Foo)}")
    assert 8 == alignment(Foo)
    assert 8 == sizeof(Foo)

if __name__ == "__main__":
    test()
