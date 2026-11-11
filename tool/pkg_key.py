#From RB1 dtServiceLow
import struct

BASE = [0xf1f97c68, 0x33bd7972, 0x01d6afdd, 0x38a224c6]
CONST_KEY = [0xde558682, 0x82d3d767, 0xab34fe1c, 0x3a04918f, 0xd7426139, 0x4dcb2fe8, 0x5bae88f1, 0x853e0275]
CONST_IV  = [0xcf50262f, 0x6c85d4db, 0x567b2808, 0xe1abf139, 0x19f13ef4, 0xb7a091ce, 0xbc40d964, 0x2ad67872]

def rol32(value, shift):
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF

def transform(base, constants, bigendian):
    b0, b1, b2, b3 = base
    result = [
        b3 ^ rol32(constants[0], 2),
        b0 ^ rol32(constants[1], 2),
        b1 ^ rol32(constants[2], 2),
        b2 ^ rol32(constants[3], 2),
        b0 ^ rol32(constants[4], 2),
        b2 ^ rol32(constants[5], 2),
        b3 ^ rol32(constants[6], 2),
        b1 ^ rol32(constants[7], 2),
    ]

    if bigendian:
        return struct.pack(">8I", *result)
    else:
        return struct.pack("<8I", *result)

key_be = transform(BASE, CONST_KEY, True)
iv_be = transform(BASE, CONST_IV, True)
print("=== Big Endian (AZ2/AZ3) ===")
print("Key:", key_be[:16].hex())
print("IV: ", iv_be[:16].hex())

key_le = transform(BASE, CONST_KEY, False)
iv_le = transform(BASE, CONST_IV, False)
print("\n=== Little Endian (RB1/RB2) ===")
print("Key:", key_le[:16].hex())
print("IV: ", iv_le[:16].hex())