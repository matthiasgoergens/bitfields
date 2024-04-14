from ctypes import Structure, c_uint, c_uint8, sizeof

# class Foo(Structure):
#     _fields_ = [("A", c_uint, 1), ("B", c_ushort, 16)]


class Foo(Structure):
    _fields_ = [
        ("A", c_uint8),
        ("B", c_uint, 16),
    ]


def test():
    print(sizeof(Foo))
    # print(sizeof(Bar))
    # assert sizeof(Foo) == sizeof(Bar)


if __name__ == "__main__":
    test()
