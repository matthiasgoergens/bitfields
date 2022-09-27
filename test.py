import ctypes
from ctypes import Structure
import string

from hypothesis import given, strategies as st, assume, note, example

unsigned = [(ctypes.c_ushort, 16), (ctypes.c_uint, 32), (ctypes.c_ulonglong, 64)]
signed = [(ctypes.c_short, 16), (ctypes.c_int, 32), (ctypes.c_longlong, 64)]
types = unsigned + signed

unsigned_types = list(zip(*unsigned))[0]
signed_types = list(zip(*signed))[0]

# ctypes.c_bool(        ctypes.c_int16(       ctypes.c_size_t(      ctypes.c_ulong(
# ctypes.c_buffer(      ctypes.c_int32(       ctypes.c_ssize_t(     ctypes.c_ulonglong(
# ctypes.c_byte(        ctypes.c_int64(       ctypes.c_ubyte(       ctypes.c_ushort(
# ctypes.c_char(        ctypes.c_int8(        ctypes.c_uint(        ctypes.c_void_p(
# ctypes.c_char_p(      ctypes.c_long(        ctypes.c_uint16(      ctypes.c_voidp(
# ctypes.c_double(      ctypes.c_longdouble(  ctypes.c_uint32(      ctypes.c_wchar(
# ctypes.c_float(       ctypes.c_longlong(    ctypes.c_uint64(      ctypes.c_wchar_p(
# ctypes.c_int(         ctypes.c_short(       ctypes.c_uint8(    

# fields = st.lists(st.tuples(st.text(), st.sampled_from([c_int, c_short, c_ulonglong]), st.integers(min_value=1)), min_size=1, max_size=10)

names = st.lists(st.text(alphabet=string.ascii_letters, min_size=1), unique=True)

@st.composite
def fields(draw, names):
    results = []
    for name in names:
        t, l = draw(st.sampled_from(types))
        results.append((name, t, draw(st.integers(min_value=1, max_value=l))))
    return results

@st.composite
def fields_and_set(draw):
    names_ = draw(names)
    
    ops = []
    results = []
    for name in names_:
        t, l = draw(st.sampled_from(types))
        res = (name, t, draw(st.integers(min_value=1, max_value=l)))
        results.append(res)
        values = draw(st.lists(st.integers()))
        for value in values:
            ops.append((res, value))
    # f = draw(fields(names))
    # assume (len(f) > 0)
    ops = draw(st.permutations(ops))
    # ops = draw(st.lists(st.tuples(st.sampled_from(f), st.integers())))
    return results, ops

@given(fops=fields_and_set())
def test(fops):
    (fields, ops) = fops
    class BITS(ctypes.Structure):
        _fields_ = fields
    b = BITS()
    for (name, t, size), i in ops:

        expect = i % (2 ** size)
        note(f"expect1: {expect} {size} {2 ** size}")
        if t not in unsigned_types:
            if expect >= 2 ** (size - 1):
                note(f"bigger: {expect} >= {2 ** (size - 1)}")
                expect -= (2 ** size)

        setattr(b, name, i)
        j = getattr(b, name)
        assert expect == j, f"{expect} != {j}"

class F(Structure):
    _fields_ = [
        ('A', ctypes.c_uint, 1),
        ('B', ctypes.c_ushort, 16)]

if __name__ == '__main__':
    test()
