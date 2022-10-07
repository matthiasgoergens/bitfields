import ctypes
import io
import math
import pathlib as p
import shlex
import string
import sys
import tempfile
import unittest
from ctypes import *
from ctypes import (
    Structure,
    alignment,
    c_char_p,
    c_int,
    c_int8,
    c_int16,
    c_int32,
    c_int64,
    c_long,
    c_uint,
    c_uint8,
    c_uint16,
    c_uint32,
    c_uint64,
    c_ulong,
    c_ulonglong,
    sizeof,
)
from dataclasses import dataclass
from struct import calcsize
from typing import *

import dataclassy as d
from hypothesis import assume, example, given, note
from hypothesis import strategies as st

unsigned = [c_uint8, c_uint16, c_uint32, c_uint64]
signed = [c_int8, c_int16, c_int32, c_int64]
# unsigned = [(ctypes.c_ushort, 16), (ctypes.c_uint, 32), (ctypes.c_ulonglong, 64)]
# signed = [(ctypes.c_short, 16), (ctypes.c_int, 32), (ctypes.c_longlong, 64)]
# types = unsigned + signed

# unsigned_types = list(zip(*unsigned))[0]
# signed_types = list(zip(*signed))[0]
types = unsigned + signed

names = st.lists(st.text(alphabet=string.ascii_uppercase, min_size=1), unique=True)

all_types = Union[
    ctypes.c_ushort,
    ctypes.c_uint,
    ctypes.c_ulonglong,
    ctypes.c_short,
    ctypes.c_int,
    ctypes.c_longlong,
]

member_t = Union[Tuple[str, all_types, int], Tuple[str, all_types]]


@d.dataclass
class StructSpec:
    pack: Optional[int]
    windows: bool
    fields: List[member_t]


DPRINT = True


def dprint(*args, **kwargs):
    if DPRINT:
        with io.StringIO() as f:
            print(*args, file=f, **kwargs, end="", flush=True)
            s = f.getvalue()
            try:
                note(s)
            except:
                print(s, flush=True)


@st.composite
def fields_and_set(draw):
    names_ = draw(names)
    ops = []
    results = []
    for name in names_:
        t = draw(st.sampled_from(types))
        if draw(st.booleans()):
            res = (name, t, draw(st.integers(min_value=1, max_value=8 * sizeof(t))))
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
            res = (name, t, draw(st.integers(min_value=1, max_value=8 * sizeof(t))))
        else:
            res = (name, t)
        results.append(res)
    return results


@st.composite
def spec_struct(draw):
    windows = draw(st.booleans())
    pack = draw(st.sampled_from([None, 1, 2, 4, 8]))
    fields = draw(fields_strat())
    # pack = draw(st.one_of(st.none(), st.integers(min_value=1, max_value=8)))
    return StructSpec(fields=fields, pack=pack, windows=windows)

@st.composite
def spec_struct_linux(draw):
    windows = False # draw(st.booleans())
    pack = None # draw(st.sampled_from([None, 1, 2, 4, 8]))
    fields = draw(fields_strat())
    # pack = draw(st.one_of(st.none(), st.integers(min_value=1, max_value=8)))
    return StructSpec(fields=fields, pack=pack, windows=windows)


def fit_in_bits(value, type_, size):
    expect = value % (2**size)
    if type_ not in unsigned:
        if expect >= 2 ** (size - 1):
            expect -= 2**size
    return expect


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


# Hmm, but how do I get my code to pretend we are in Windows land?
# Needs trickery.  Perhaps recompile for this.


def normalise1(member: member_t) -> Tuple[str, all_types, int]:
    # This code contributed by copilot.
    if len(member) == 2:
        return member[0], member[1], 8 * sizeof(member[1])
    else:
        return member


members_t = List[member_t]


@d.dataclass
class Bitfield:
    start: int
    size: int
    end: int = None

    def __post_init__(self):
        self.end = self.start + self.size


# Afterwards, we need to adjust the total size to the maximum alignment of any field.
def old_layout(spec: StructSpec):
    # We want to figure out the sizeof the struct, and the offset of each field.

    # For purposes of the algorithm, we can normalize members that are not-bitfields, to be bitfields of the full size of the type.
    members: List[Tuple[str, all_types, int]] = list(map(normalise1, spec.fields))

    pack = spec.pack or math.inf
    windows = spec.windows or (spec.pack is not None)

    # Do everything in bits?
    # and worry about alignment.
    offset = 0
    alignments = []
    # Need start, size and end of bitfield.  If any.
    # Only needs this for Windows..
    if windows:
        bitfield = Bitfield(0, 0, 0)
    for name, type_, bitsize in members:
        dprint(f"name: {name}, type: {type_}, bitsize: {bitsize}")
        align = 8 * min(alignment(type_), pack)
        alignments.append(align)
        if windows:
            if 8 * alignment(type_) != bitfield.size or bitfield.end < offset + bitsize:
                dprint(f"new bitfield. old: {bitfield}")
                dprint(
                    f"8 * alignment(type_) { alignment(type_)} ?!= bitfield.size {bitfield.size}"
                )
                dprint(
                    f"bitfield.end {bitfield.end} ?<= offset {offset} + bitsize {bitsize}"
                )
                # offset = bitfield.end
                assert offset <= bitfield.end
                offset = bitfield.end
                offset = round_up1(offset, align)
                bitfield = Bitfield(start=offset, size=8 * alignment(type_))
                dprint(f"new bitfield. new: {bitfield}")

        # detect alignment straddles
        def straddles(x):
            return round_down(x, align) < round_down(x + bitsize - 1, align)

        if spec.pack is None and straddles(offset):
            assert not windows
            dprint(f"straddles: {offset} {align} {bitsize}")
            offset = round_up(offset, align)
            assert pack is not None or not straddles(offset)

        offset += bitsize
    if windows:
        note(f"offset: {offset}\tbitfield.end: {bitfield.end}")
        # in case we had an open bitfield, we need to close it.
        assert offset <= bitfield.end
        offset = bitfield.end
    dprint("offset", offset)
    total_alignment = max(alignments, default=8) // 8
    total_size = round_up(offset, 8 * total_alignment) // 8
    dprint("total_size", total_size)
    return total_alignment, total_size


def layout_windows(spec: StructSpec):
    # We want to figure out the sizeof the struct, and the offset of each field.

    # For purposes of the algorithm, we can normalize members that are not-bitfields, to be bitfields of the full size of the type.
    members: List[Tuple[str, all_types, int]] = list(map(normalise1, spec.fields))

    pack = spec.pack or math.inf
    windows = spec.windows or (spec.pack is not None)
    assert windows

    # Do everything in bits?
    # and worry about alignment.
    offset = 0
    alignments = []
    # Need start, size and end of bitfield.  If any.
    # Only needs this for Windows..

    bitfield = Bitfield(0, 0)
    for name, type_, bitsize in members:
        align = 8 * min(alignment(type_), pack)
        alignments.append(align)

        if bitfield.end < offset + bitsize or 8 * sizeof(type_) != bitfield.size:
            assert offset <= bitfield.end
            offset = bitfield.end

            offset = round_up(offset, align)
            bitfield = Bitfield(start=offset, size=8 * sizeof(type_))

        offset += bitsize

    assert offset <= bitfield.end
    offset = bitfield.end

    total_alignment = max(alignments, default=8) // 8
    total_size = round_up(offset, 8 * total_alignment) // 8
    return total_alignment, total_size


def layout_linux(spec: StructSpec):
    # We want to figure out the sizeof the struct, and the offset of each field.

    # For purposes of the algorithm, we can normalize members that are not-bitfields, to be bitfields of the full size of the type.
    members: List[Tuple[str, all_types, int]] = list(map(normalise1, spec.fields))

    windows = spec.windows or (spec.pack is not None)
    assert not windows

    offset = 0
    alignments = []
    for name, type_, bitsize in members:
        align = 8 * alignment(type_)
        alignments.append(align)

        offset = max(offset, round_down(offset + bitsize - 1, align))
        # assert: no alignment straddle
        assert round_down(offset, align) >= round_down(offset + bitsize - 1, align)

        offset += bitsize
    total_alignment = max(alignments, default=8) // 8
    total_size = round_up(offset, 8 * total_alignment) // 8
    return total_alignment, total_size


def layout(spec: StructSpec):
    pack = spec.pack or math.inf
    windows = spec.windows or (spec.pack is not None)
    if windows:
        return layout_windows(spec)
    else:
        return layout_linux(spec)


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
            return f"    {c_name(type_)} {name};"
        case (name, type_, size):
            return f"    {c_name(type_)} {name}: {size};"


def c_format(fields: members_t) -> str:
    return "\n".join(map(c_format1, fields))


def make_c(spec: StructSpec):
    if spec.pack is not None:
        pragma = f"#pragma pack({spec.pack})"
    else:
        pragma = ""
    if spec.pack is not None or spec.windows:
        attribute = "__attribute__ ((ms_struct))"
    else:
        attribute = ""

    return f"""
#include<stdio.h>
#include<inttypes.h>

{pragma}

typedef struct
{attribute}
{{
{c_format(spec.fields)}
}} Foo;

int main(int argc, char** argv) {{
    printf("%lu\\n", __alignof__(Foo));
    printf("%lu\\n", sizeof(Foo));
    return 0;
}}
"""


def get_from_c(spec):
    with tempfile.TemporaryDirectory() as d:
        d: p.Path = p.Path(d)
        f = d / "gen.c"
        out = d / "a.out"
        f.write_text(make_c(spec))
        sp.run((*shlex.split("clang -fsanitize=undefined -Wall -O0 -o"), out, f))
        proc = sp.run([out], capture_output=True)
        align_, sizeof_ = map(int, proc.stdout.split())
        return align_, sizeof_


from ctypes import c_ushort


class Test_Bitfields(unittest.TestCase):
    def test_mixed_5_original(self):
        class X(Structure):
            _fields_ = [("A", c_uint, 1), ("B", c_ushort, 16)]

        a = X()
        a.A = 0
        a.B = 1
        self.assertEqual(1, a.B)

    def test_mixed_5(self):
        class X(Structure):
            _fields_ = [("A", c_uint32, 1), ("B", c_uint16, 16)]

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
        align_, size_ = layout(StructSpec(fields=fields, pack=None, windows=False))
        assert 4 == size_

        class X(Structure):
            _fields_ = fields

        self.assertEqual(4, sizeof(X))

    @given(spec=spec_struct())
    def test_layout_against_old(self, spec):
        note(make_c(spec))
        self.assertEqual(old_layout(spec), layout(spec), "align_, size_")

    @given(spec=spec_struct())
    def test_layout_against_c(self, spec):
        note(make_c(spec))
        self.assertEqual(get_from_c(spec), layout(spec), "align_, size_")

    # TODO: make general!
    @given(spec=spec_struct())
    # @given(spec=spec_struct_linux())
    def test_structure_against_c(self, spec):
        assume(not (spec.pack is None and spec.windows))

        align_, sizeof_ = get_from_c(spec)
        # print(align_, sizeof_)

        if spec.pack is None:

            class X(Structure):
                _fields_ = spec.fields

        else:
            print(spec, flush=True, file=open('log.txt', 'a'))
            class X(Structure):
                _pack_ = spec.pack
                _fields_ = spec.fields

        self.assertEqual(sizeof_, sizeof(X), "sizeof doesn't match")
        self.assertEqual(align_, alignment(X), "alignment doesn't match")

    def test_struct_example(self):
        class X(Structure):
            _pack_ = 1
            _fields_ = [('A', c_uint8)]
        # StructSpec(pack=1, windows=False, fields=[('A', <class 'ctypes.c_ubyte'>)])

    def test_struct_example2(self):
        class X(Structure):
            _pack_ = 1
            _fields_ = fields=[('IRF', ctypes.c_int, 17), ('OLIEG', c_ushort), ('EMZTTMFWIYXUIXRFEVFMSK', ctypes.c_uint, 19), ('VDTFOKUTVGDUBYK', ctypes.c_byte)]


    def test_structures(self):
        WNDPROC = ctypes.CFUNCTYPE(c_long)

        def wndproc():
            return 0

        class WNDCLASS(Structure):
            _fields_ = [("lpfnWndProc", WNDPROC)]

        dprint("WNDCLASS align", alignment(WNDCLASS))
        dprint("WNDCLASS sizeof", sizeof(WNDCLASS))

        wndclass = WNDCLASS()
        tmp = WNDPROC(wndproc)
        dprint("WNDPROC align", alignment(WNDPROC))
        dprint("WNDPROC sizeof", sizeof(WNDPROC))
        wndclass.lpfnWndProc = tmp
        return
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

    formats = {
        "c": c_char,
        "b": c_byte,
        "B": c_ubyte,
        "h": c_short,
        "H": c_ushort,
        "i": c_int,
        "I": c_uint,
        "l": c_long,
        "L": c_ulong,
        "q": c_longlong,
        "Q": c_ulonglong,
        "f": c_float,
        "d": c_double,
    }

    def test_unions(self):
        for code, tp in self.formats.items():

            class X(ctypes.Union):
                _fields_ = [("x", c_char), ("y", tp)]

            self.assertEqual((sizeof(X), code), (calcsize("%c" % (code)), code))

    def test_mixed_2(self):
        class X(Structure):
            _fields_ = [("a", c_byte, 4), ("b", c_int, 32)]

        self.assertEqual(sizeof(X), alignment(c_int) + sizeof(c_int))


# TODO: perhaps also check that we have the same layout as C?
# by creating random assignments.
# and checking via unions?

if __name__ == "__main__":
    import tracemalloc

    tracemalloc.start()
    DPRINT = True
    t = Test_Bitfields()
    # t.test_mixed_2()
    # t.test_structures()
    t.test_struct_example()
    t.test_struct_example2()
    # t.test_structure_against_c()

    # fields=[('A', ctypes.c_ubyte, 1)]
    # print(layout(fields))
