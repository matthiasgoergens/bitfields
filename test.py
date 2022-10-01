import ctypes
from ctypes import alignment,sizeof, Structure, c_ulonglong
from ctypes import c_uint, c_uint8, c_uint16, c_uint32, c_uint64, c_ulong
from ctypes import c_int, c_int8, c_int16, c_int32, c_int64, c_long
import string
import shlex
import unittest


from hypothesis import assume, example, given, note
from hypothesis import strategies as st
from typing import *

import sys
import tempfile
import pathlib as p

unsigned = [c_uint8, c_uint16, c_uint32, c_uint64]
signed = [c_int8, c_int16, c_int32, c_int64]
# unsigned = [(ctypes.c_ushort, 16), (ctypes.c_uint, 32), (ctypes.c_ulonglong, 64)]
# signed = [(ctypes.c_short, 16), (ctypes.c_int, 32), (ctypes.c_longlong, 64)]
# types = unsigned + signed

# unsigned_types = list(zip(*unsigned))[0]
# signed_types = list(zip(*signed))[0]
types = unsigned + signed

names = st.lists(st.text(alphabet=string.ascii_letters, min_size=1), unique=True)


@st.composite
def fields_and_set(draw):
    names_ = draw(names)
    ops = []
    results = []
    for name in names_:
        t = draw(st.sampled_from(types))
        if draw(st.booleans()):
            res = (name, t, draw(st.integers(min_value=1, max_value=8*sizeof(t))))
        else:
            res = (name, t)
        results.append(res)
        values = draw(st.lists(st.integers()))
        for value in values:
            ops.append((res, value))
    ops = draw(st.permutations(ops))
    return results, ops


@st.composite
def fields_strat(draw):
    names_ = draw(names)
    results = []
    for name in names_:
        t = draw(st.sampled_from(types))
        if draw(st.booleans()):
            res = (name, t, draw(st.integers(min_value=1, max_value=8*sizeof(t))))
        else:
            res = (name, t)
        results.append(res)
    return results

def fit_in_bits(value, type_, size):
    expect = value % (2**size)
    if type_ not in unsigned:
        if expect >= 2 ** (size - 1):
            expect -= 2**size
    return expect


all_types = Union[
    ctypes.c_ushort, ctypes.c_uint, ctypes.c_ulonglong,
    ctypes.c_short, ctypes.c_int, ctypes.c_longlong,
]

def round_up(x, y):
    return ((x - 1) // y + 1) * y

def round_down(x, y):
    return (x // y) * y

member_t = Union[Tuple[str, all_types, int], Tuple[str, all_types]]

def normalise1(member: member_t) -> Tuple[str, all_types, int]:
    # This code contributed by copilot.
    if len(member) == 2:
        return member[0], member[1], 8 * sizeof(member[1])
    else:
        return member

members_t = List[member_t]

# Afterwards, we need to adjust the total size to the maximum alignment of any field.
def layout(members: members_t):
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
            print(f"straddles: {offset} {align} {bitsize}")
            offset = round_up(offset, align)
            assert not straddles(offset)

        offset += bitsize
    print(offset)
    total_size = round_up(offset, 8 * max(alignment(type_) for name, type_, bitsize in members)) // 8
    print(total_size)
    return total_size


def c_name(type_: all_types) -> str:
    return {
        c_uint: "unsigned int",
        c_uint8: "uint8_t",
        c_uint16: "uint16_t",
        c_uint32: "uint32_t",
        c_uint64: "uint64_t",

        c_int8: "int8_t",
        c_int16: "int16_t",
        c_int32: "int32_t",
        c_int64: "int64_t",
    }[type_]

import subprocess as sp

def c_format1(field: member_t) -> str:
    match field:
        case (name, type_):
            return f"    {c_name(type_)} {name};\n"
        case (name, type_, size):
            return f"    {c_name(type_)} {name}: {size};\n"

def c_format(fields: members_t) -> str:
    return ''.join(map(c_format1, fields))

def make_c(fields):
    return f"""
#include<stdio.h>
#include<inttypes.h>

typedef struct
{{
{c_format(fields)}
}} Foo;

int main(int argc, char** argv) {{
    printf("%lu\\n", __alignof__(Foo));
    printf("%lu\\n", sizeof(Foo));
    return 0;
}}
"""



"""
rm -f a.out; clang -fsanitize=undefined -Wall -Os gen.c && ./a.out
"""

class Test_C(unittest.TestCase):
    def test_layout(self):
        fields = [
            ("A", c_uint8),
            ("B", c_uint, 16),
            ]
        assert layout(fields) == 4
        class X(Structure):
            _fields_ = fields
        self.assertEqual(4, sizeof(X))


    @given(fops=fields_and_set())
    def test_roundtrip(self, fops):
        (fields, ops) = fops

        class BITS(ctypes.Structure):
            _fields_ = fields

        b = BITS()
        for x, value in ops:
            (name, type_, size) = normalise1(x)

            expect = fit_in_bits(value, type_, size)
            setattr(b, name, value)
            j = getattr(b, name)
            self.assertEqual(expect, j)

    @given(fields=fields_strat())
    def test_c(self, fields):
        with tempfile.TemporaryDirectory() as d:
            d: p.Path = p.Path(d)
            f = d / 'gen.c'
            out = d / 'a.out'
            f.write_text(make_c(fields))
            sp.run((*shlex.split("clang -fsanitize=undefined -Wall -O0 -o"), out, f))
            proc = sp.run([out], capture_output=True)
            align_, sizeof_ = map(int, proc.stdout.split())
            # print(align_, sizeof_)

            class X(Structure):
                _fields_ = fields
            self.assertEqual(sizeof_, sizeof(X), "sizeof doesn't match")
            self.assertEqual(align_, alignment(X), "alignment doesn't match")

            # sys.stdout.write(f.read_text())

# if __name__ == "__main__":
#     # test_layout()
#     t = Test_C()
#     # test()
#     Test_C().test_c()
