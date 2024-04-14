from ctypes import *


class X(Structure):
    _ms_struct_ = True
    _fields_ = [
        ("A", c_ubyte),
        ("B", c_ushort, 1),
    ]


print(sizeof(X))
print(sizeof(c_ushort))

"""
E       spec=StructSpec(pack=None, windows=True, fields=[MemberSpec(name='A', type=<class 'ctypes.c_ubyte'>, bitsize=None, value=0), MemberSpec(name='B', type=<class 'ctypes.c_ushort'>, bitsize=1, value=0)]),
"""
