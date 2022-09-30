from ctypes import Structure, c_uint, c_ulonglong, c_ushort
from ctypes import sizeof
import ctypes


# class Foo(Structure):
#     _fields_ = [("A", c_uint, 1), ("B", c_ushort, 16)]


class Foo(Structure):
    _fields_ = [
        ("A", c_uint),
        ("B", c_uint, 32),
        ("C", c_ulonglong, 1),
        ]

class Bar(Structure):
    _fields_ = [
        ("A", c_uint),
        ("B", c_uint),
        ("C", c_ulonglong, 1),
        ]


def test():
    print(sizeof(Foo))
    print(sizeof(Bar))
    assert sizeof(Foo) == sizeof(Bar)

if __name__ == "__main__":
    test()
