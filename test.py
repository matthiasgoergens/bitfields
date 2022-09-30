import ctypes
from ctypes import alignment, sizeof
import string

from hypothesis import assume, example, given, note
from hypothesis import strategies as st
from typing import *

unsigned = [(ctypes.c_ushort, 16), (ctypes.c_uint, 32), (ctypes.c_ulonglong, 64)]
signed = [(ctypes.c_short, 16), (ctypes.c_int, 32), (ctypes.c_longlong, 64)]
types = unsigned + signed

unsigned_types = list(zip(*unsigned))[0]
signed_types = list(zip(*signed))[0]
raw_types = unsigned_types + signed_types

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
    if type_ not in unsigned_types:
        if expect >= 2 ** (size - 1):
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


all_types = Union[
    ctypes.c_ushort, ctypes.c_uint, ctypes.c_ulonglong,
    ctypes.c_short, ctypes.c_int, ctypes.c_longlong,
]

def round_up(x, y):
    return ((x - 1) // y + 1) * y

def round_down(x, y):
    return (x // y) * y

def normalise1(member: Union[Tuple[str, all_types, int], Tuple[str, all_types]) -> Tuple[str, all_types, int]:
    # This code contributed by copilot.
    if len(member) == 2:
        return member[0], member[1], 8 * sizeof(member[1])
    else:
        return member

# Afterwards, we need to adjust the total size to the maximum alignment of any field.
def layout(members: List[Union[Tuple[str, all_types, int], Tuple[str, all_types]]]):
    # We want to figure out the sizeof the struct, and the offset of each field.
    
    # For purposes of the algorithm, we can normalize members that are not-bitfields, to be bitfields of the full size of the type.
    members: List[Tuple[str, all_types, int]] = list(map(normalise1, members))

    # Do everything in bits?
    # and worry about alignment.
    offset = 0
    for name, type_, bitsize in members:
        align = 8 * alignment(type_)

        # detect alignment straddles
        def straddles(x):
            return round_down(x, align) < round_down(x + bitsize - 1, align)
        if straddles(offset):
            offset = round_up(offset, align)
            assert not straddles(ofset)

        offset += bitsize
    return round_up(offset, 8 * max(alignment(type_) for name, type_, bitsize in members)) // 8


if __name__ == "__main__":
    test()
