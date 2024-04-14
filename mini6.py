from ctypes import Structure, c_uint, c_ushort, sizeof


class Foo(Structure):
    _fields_ = [
        ("A", c_ushort),
        ("B", c_ushort),
        ("C", c_ushort),
        ]

class Bar(Structure):
    _fields_ = [
        ("A", c_uint),
        ("C", c_ushort),
        ]

def test():
    print(sizeof(Foo))
    print(sizeof(Bar))
    assert 6 == sizeof(Foo)
    assert 8 == sizeof(Bar)

if __name__ == "__main__":
    test()
