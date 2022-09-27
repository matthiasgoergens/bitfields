import ctypes
import string

from hypothesis import assume, example, given, note
from hypothesis import strategies as st

unsigned = [(ctypes.c_ushort, 16), (ctypes.c_uint, 32), (ctypes.c_ulonglong, 64)]
signed = [(ctypes.c_short, 16), (ctypes.c_int, 32), (ctypes.c_longlong, 64)]
types = unsigned + signed

unsigned_types = list(zip(*unsigned))[0]
signed_types = list(zip(*signed))[0]

names = st.lists(st.text(alphabet=string.ascii_letters, min_size=1), unique=True)


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
    ops = draw(st.permutations(ops))
    return results, ops


def fit_in_bits(value, type_, size):
    expect = value % (2**size)
    note(f"expect1: {expect} {size} {2 ** size}")
    if type_ not in unsigned_types:
        if expect >= 2 ** (size - 1):
            note(f"bigger: {expect} >= {2 ** (size - 1)}")
            expect -= 2**size
    return expect


@given(fops=fields_and_set())
def test(fops):
    (fields, ops) = fops

    class BITS(ctypes.Structure):
        _fields_ = fields

    b = BITS()
    for (name, type_, size), value in ops:

        expect = fit_in_bits(value, type_, size)
        setattr(b, name, value)
        j = getattr(b, name)
        assert expect == j, f"{expect} != {j}"


if __name__ == "__main__":
    test()
