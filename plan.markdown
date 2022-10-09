So far I have tested `sizeof` and `__alignof__` only, and they work.

But we should also test the actual assignment of the values.

In C: use calloc to get zeroed memory.  Fill with values.  Write out to disk.

In Python: read back in and parse with ctypes' cstruct.  Check that the values are the same.

Alternative:
In Python: create the same struct, and use `pack` to write it out.  Check that the bytes are the same as in the C version.

Done!

Now for the big endian version.

Check what Python does right now.  As far as I can tell, it's a mess.

--

Ok, I think the existing location for the bitfield reversing works, even if it's a bit weird.

But we can implement it as a post-processing step!
