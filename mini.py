from ctypes import Structure, c_uint, c_ushort, c_ulonglong

class Foo(Structure):
    _fields_ = [
        ('A', c_uint, 1),
        ('B', c_ushort, 16)]

class Bar(Structure):
    _fields_ = [
        ('A', c_ulonglong, 1),
        ('B', c_uint, 32)]

if __name__ == "__main__":
    for a in [Foo(), Bar()]:
        a = Foo()
        a.A = 0
        a.B = 1
        print(a.A, a.B)
