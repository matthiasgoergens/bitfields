# import ctypes

# for field_width in range(32, 1, -1):
#     class TestStruct(ctypes.Structure):
#         _fields_ = [
#             ("Field1", ctypes.c_uint32, field_width),
#             ("Field2", ctypes.c_uint8, 8)
#         ]

#     cmd = TestStruct()
#     cmd.Field2 = 1
#     if cmd.Field2 != 1:
#         raise RuntimeError(f"{field_width=}, {cmd.Field2=} != 1")

# print("All good")

from ctypes import Structure, Union
from ctypes import alignment, sizeof
from ctypes import c_int8, c_int16, c_int32, c_int64
from ctypes import c_uint8, c_uint16, c_uint32, c_uint64


class sub_type(Structure):
    # _pack_ = 1
    _ms_struct_ = True
    _fields_ = [
        # ('_', c_uint64, 1),
        ("a", c_uint8, 4),
        ("b", c_uint8, 4),
        ("c", c_uint16, 10),
        ("d", c_uint16, 10),
        ("e", c_uint8, 1),
        ("f", c_uint8, 1),
        ("g", c_uint8, 1),
    ]


class main_type(Union):
    # _ms_struct_ = True
    byte_length = sizeof(sub_type)
    _fields_ = [
        ("data", sub_type),
        ("asbytes", c_uint8 * byte_length),
    ]


a = main_type(data=sub_type(e=1, f=1, g=1))
print(sizeof(sub_type))
print(sizeof(a))
print(a.data.e, a.data.f, a.data.g)
print(list(a.asbytes))
print(list(map(bin, a.asbytes)))

# on windows, print value is correct
# [0, 0, 0, 0, 0, 0, 7, 0]

# on linux, the value is wrong at all. the length is correct, but value is wrong.
# [0, 0, 0, 0, 0, 0]`
