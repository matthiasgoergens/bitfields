import ctypes
from ctypes import c_char_p
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

try:
    WINFUNCTYPE
except NameError:
    # fake to enable this test on Linux
    WINFUNCTYPE = ctypes.CFUNCTYPE

unsigned = [c_uint8, c_uint16, c_uint32, c_uint64]
signed = [c_int8, c_int16, c_int32, c_int64]
# unsigned = [(ctypes.c_ushort, 16), (ctypes.c_uint, 32), (ctypes.c_ulonglong, 64)]
# signed = [(ctypes.c_short, 16), (ctypes.c_int, 32), (ctypes.c_longlong, 64)]
# types = unsigned + signed

# unsigned_types = list(zip(*unsigned))[0]
# signed_types = list(zip(*signed))[0]
types = unsigned + signed

names = st.lists(st.text(alphabet=string.ascii_uppercase, min_size=1), unique=True)


DPRINT=True

def dprint(*args, **kwargs):
    if DPRINT:
        print(*args, **kwargs)


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

def round_down(x, y):
    return (x // y) * y

def round_up(x, y):
    return -round_down(-x, y)

def round_up1(x, y):
    return ((x - 1) // y + 1) * y

class Test_round(unittest.TestCase):
    @given(x=st.integers(), y=st.integers())
    def test_round(self, x, y):
        assume(y > 0)
        self.assertEqual(round_up1(x, y), round_up(x, y))

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
            dprint(f"straddles: {offset} {align} {bitsize}")
            offset = round_up(offset, align)
            assert not straddles(offset)

        offset += bitsize
    dprint('offset', offset)
    total_alignment = max((alignment(type_) for name, type_, bitsize in members), default=1)
    total_size = round_up(offset, 8 * total_alignment) // 8
    dprint('total_size', total_size)
    return total_alignment, total_size


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

def get_from_c(fields):
    with tempfile.TemporaryDirectory() as d:
        d: p.Path = p.Path(d)
        f = d / 'gen.c'
        out = d / 'a.out'
        f.write_text(make_c(fields))
        sp.run((*shlex.split("clang -fsanitize=undefined -Wall -O0 -o"), out, f))
        proc = sp.run([out], capture_output=True)
        align_, sizeof_ = map(int, proc.stdout.split())
        return align_, sizeof_

from ctypes import c_ushort

class Test_Bitfields(unittest.TestCase):
    def test_mixed_5_original(self):
        class X(Structure):
            _fields_ = [
                ('A', c_uint, 1),
                ('B', c_ushort, 16)]
        a = X()
        a.A = 0
        a.B = 1
        self.assertEqual(1, a.B)

    def test_mixed_5(self):
        class X(Structure):
            _fields_ = [
                ('A', c_uint32, 1),
                ('B', c_uint16, 16)]
        a = X()
        a.A = 0
        a.B = 1
        self.assertEqual(1, a.B)

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

    def test_layout(self):
        """This is a special case of test_c"""
        fields = [
            ("A", c_uint8),
            ("B", c_uint, 16),
            ]
        align_, size_ = layout(fields)
        assert 4 == size_
        class X(Structure):
            _fields_ = fields
        self.assertEqual(4, sizeof(X))

    @given(fields=fields_strat())
    def test_layout_against_c(self, fields):
        self.assertEqual(get_from_c(fields), layout(fields), "align_, size_")
        

    @given(fields=fields_strat())
    def test_structure_against_c(self, fields):
        align_, sizeof_ = get_from_c(fields)
        # print(align_, sizeof_)

        class X(Structure):
            _fields_ = fields
        self.assertEqual(sizeof_, sizeof(X), "sizeof doesn't match")
        self.assertEqual(align_, alignment(X), "alignment doesn't match")

    def test_structures(self):
        WNDPROC = WINFUNCTYPE(c_long, c_int, c_int, c_int, c_int)

        def wndproc(hwnd, msg, wParam, lParam):
            return hwnd + msg + wParam + lParam

        HINSTANCE = c_int
        HICON = c_int
        HCURSOR = c_int
        LPCTSTR = c_char_p

        class WNDCLASS(Structure):
            _fields_ = [("style", c_uint),
                        ("lpfnWndProc", WNDPROC),
                        ("cbClsExtra", c_int),
                        ("cbWndExtra", c_int),
                        ("hInstance", HINSTANCE),
                        ("hIcon", HICON),
                        ("hCursor", HCURSOR),
                        ("lpszMenuName", LPCTSTR),
                        ("lpszClassName", LPCTSTR)]

        wndclass = WNDCLASS()
        wndclass.lpfnWndProc = WNDPROC(wndproc)

        WNDPROC_2 = WINFUNCTYPE(c_long, c_int, c_int, c_int, c_int)

        # This is no longer true, now that WINFUNCTYPE caches created types internally.
        ## # CFuncPtr subclasses are compared by identity, so this raises a TypeError:
        ## self.assertRaises(TypeError, setattr, wndclass,
        ##                  "lpfnWndProc", WNDPROC_2(wndproc))
        # instead:

        self.assertIs(WNDPROC, WNDPROC_2)
        # 'wndclass.lpfnWndProc' leaks 94 references.  Why?
        self.assertEqual(wndclass.lpfnWndProc(1, 2, 3, 4), 10)


        f = wndclass.lpfnWndProc

        del wndclass
        del wndproc

        self.assertEqual(f(10, 11, 12, 13), 46)

# TODO: perhaps also check that we have the same layout as C?
# by creating random assignments.
# and checking via unions?

if __name__ == "__main__":
    DPRINT=True
    t = Test_Bitfields()
    t.test_structures()

    # fields=[('A', ctypes.c_ubyte, 1)]
    # print(layout(fields))
