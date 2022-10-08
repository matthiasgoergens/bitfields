import ctypes


class Bad(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("a0", ctypes.c_uint8, 1),
        ("a1", ctypes.c_uint8, 1),
        ("a2", ctypes.c_uint8, 1),
        ("a3", ctypes.c_uint8, 1),
        ("a4", ctypes.c_uint8, 1),
        ("a5", ctypes.c_uint8, 1),
        ("a6", ctypes.c_uint8, 1),
        ("a7", ctypes.c_uint8, 1),
        ("b0", ctypes.c_uint16, 4),
        ("b1", ctypes.c_uint16, 12),
    ]


class GoodA(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("a0", ctypes.c_uint8, 1),
        ("a1", ctypes.c_uint8, 1),
        ("a2", ctypes.c_uint8, 1),
        ("a3", ctypes.c_uint8, 1),
        ("a4", ctypes.c_uint8, 1),
        ("a5", ctypes.c_uint8, 1),
        ("a6", ctypes.c_uint8, 1),
        ("a7", ctypes.c_uint8, 1),
    ]


class Good(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("a", GoodA),
        ("b0", ctypes.c_uint16, 4),
        ("b1", ctypes.c_uint16, 12),
    ]


def printCTypeOffsets(cStruct):
    for f in cStruct._fields_:
        ft = getattr(cStruct, f[0])
        print(ft.offset, hex(ft.size), f[0])


print("Size is ", ctypes.sizeof(Bad), "Expected 3")
printCTypeOffsets(Bad)

print("Size is ", ctypes.sizeof(Good), "Expected 3")
printCTypeOffsets(Good)
