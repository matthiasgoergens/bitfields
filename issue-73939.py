from ctypes import *


class MyStructure(Structure):
    _pack_      = 1
    _fields_    = [ 
                      ("P",       c_uint16),
                      ("L",       c_uint16, 9),
                      ("Pro",     c_uint16, 1),
                      ("G",       c_uint16, 1),
                      ("IB",      c_uint16, 1),
                      ("IR",      c_uint16, 1),
                      ("R",       c_uint16, 3),
                      ("T",       c_uint32, 10),
                      ("C",       c_uint32, 20),
                      ("R2",      c_uint32, 2)
                  ]

print (sizeof(MyStructure))


# Windows seems to correctly report 8
# Linux seems to (incorrectly) report 10
