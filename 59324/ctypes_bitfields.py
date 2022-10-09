import itertools
import os
import random
import shutil
import subprocess
import tempfile

from ctypes import Structure, c_ulong, c_uint, c_ushort, c_ubyte, sizeof


c_code_template = """\
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <string.h>

struct flags {{
{fields}\
}};

int main(void) {{
  struct flags my_flags;
  unsigned char buffer[1000];
  memset(&my_flags, 0, sizeof(my_flags));
  memset(buffer, 0, sizeof(buffer));

{write_field_mask}\
  return 0;
}}
"""

write_field_mask_template = """\
  /* Set {name} to all 1s. */
  my_flags.{name} = {all_ones}U;
  memcpy(buffer, &my_flags, sizeof(my_flags));
  write(1, buffer, sizeof(my_flags));
  my_flags.{name} = 0;

"""


def names():
    """Generate distinct alphabetic names. """
    for length in itertools.count(1):
        for name in itertools.product('abcdefgh', repeat=length):
            yield ''.join(name)

int_type_name = {
    c_ulong: 'unsigned long',
    c_uint: 'unsigned int',
    c_ushort: 'unsigned short',
    c_ubyte: 'unsigned char',
}

int_types = list(int_type_name.keys())


def ctypes_layout(flags):
    ctypes_fields = []
    for name, (ctype, width) in zip(names(), flags):
        if width is None:
            ctypes_fields.append((name, ctype))
        else:
            ctypes_fields.append((name, ctype, width))


    class BITS(Structure):
        _fields_ = ctypes_fields

    for name, (ctype, requested_width) in zip(names(), flags):
        field = getattr(BITS, name)
        if requested_width is None:
            width = 8 * field.size
            start = 0
            yield field.offset, start, width
        else:
            # width, start = divmod(field.size, 65536)
            width = field.size >> 16
            start = field.size & 0xffff
            assert (width, start) == divmod(field.size, 65536), ((width, start), divmod(field.size, 65536))
            yield field.offset, start, width


def simulated_layout(flags):
    bitpos = 0
    for ctype, width in flags:
        if width is None:
            # Plain old integer field (not a bitfield)
            width = 8 * sizeof(ctype)
        space = -bitpos % (8 * sizeof(ctype))
        if width > space:
            bitpos += space
        offset, start = divmod(bitpos, 8 * sizeof(ctype))
        yield offset * sizeof(ctype), start, width
        bitpos += width


def render_code(flags):
    flag_descriptions = []
    write_field_mask_bits = []
    for (type, width), name in zip(flags, names()):
        if width is not None:
            descr_template = "  {type} {name}: {width};\n"
        else:
            descr_template = "  {type} {name};\n"
        descr = descr_template.format(
            type=int_type_name[type],
            name=name,
            width=width,
        )
        flag_descriptions.append(descr)

        if width is None:
            width = sizeof(type) * 8

        write_field_mask_bits.append(write_field_mask_template.format(
                name=name,
                all_ones=str(2 ** width - 1),
            ))
    fields = ''.join(flag_descriptions)
    write_field_mask = ''.join(write_field_mask_bits)
    return c_code_template.format(
        fields=fields,
        write_field_mask=write_field_mask,
    )


def compile_and_execute(c_code):
    tmpdir = tempfile.mkdtemp()
    try:
        infile = os.path.join(tmpdir, 'test.c')
        outfile = os.path.join(tmpdir, 'test')
        with open(infile, 'w') as f:
            f.write(c_code)
        args = ['gcc', '-Wall', '-Wextra', infile, '-o', outfile]
        subprocess.check_call(args)
        output = subprocess.check_output([outfile])
    finally:
        shutil.rmtree(tmpdir)

    return output


def actual_layout(flags):
    c_code = render_code(flags)
    output = compile_and_execute(c_code)

    # Analyze the output.
    assert len(output) % len(flags) == 0
    piece_size = len(output) // len(flags)

    for i, (ctype, width) in enumerate(flags):
        chunk = output[i * piece_size:(i + 1) * piece_size]
        assert len(chunk) == piece_size
        n = int.from_bytes(chunk, byteorder='little')
        start = ((n - 1) & ~n).bit_length()
        end = n.bit_length()
        if width is None:
            width = sizeof(ctype) * 8
        try:
            assert end - start == width, f"{end} - {start} == {end - start} == {width}"
        except:
            print(f"chunk: {[hex(x) for x in reversed(chunk)]}")
            print(f"i: {i}")
            print(f"n: {n:x}")
            print(f"flags: {flags}")
            print(f"c_code:\n{c_code}")
            raise
        assert n == 2 ** end - 2 ** start

        bit_offset = start % (sizeof(ctype) * 8)
        byte_offset = (start - bit_offset) // 8
        yield byte_offset, bit_offset, width


def random_flag():
    ctype = random.choice(int_types)
    if random.choice([False, True]):
        # bitfield
        size = random.randrange(sizeof(ctype) * 8) + 1
    else:
        # full field
        size = None
    return ctype, size


def random_flags(size):
    return [random_flag() for _ in range(size)]


def random_test(size=3):
    flags = random_flags(size=size)
    c = list(ctypes_layout(flags))
    s = list(simulated_layout(flags))
    a = list(actual_layout(flags))
    if not a == s == c:
        print(f"flags: {flags}")
        print("field.offset, start, width")
        print("ctypes:    ", c)
        print("simulated: ", s)
        print("actual:    ", a)
        c_code = render_code(flags)
        print(f"c_code:\n{c_code}")
        assert False


def main():
    random.seed(0)
    for size in range(2, 10):
        print("size: ", size)
        for i in range(1000):
            random_test(size)


if __name__ == '__main__':
    main()

