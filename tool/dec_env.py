# decryption scheme for the Environment file/area, on EEGS this is the only layer used, on NX there is also an AES layer above it

import sys

SERIAL = "A-1084-689-B_2015117"     #eegs

def env_crypt(data, key):
    buf = bytearray(data)
    key_bytes = key.encode("latin1")

    #special mode
    legacy_mode = len(key_bytes) == 4 and key_bytes[0] < ord("4")

    state = 0xDEADBEAF  # yes - DEAD BEAF

    for c in key_bytes:
        state = ((state * 4) + c) & 0xFFFFFFFF

    last = len(buf) - 1
    while last >= 0 and buf[last] == 0xFF:
        last -= 1

    for i in range(last + 1):
        state = (state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF

        if legacy_mode:
            k = state & 0xFF
        else:
            k = (
                (state & 0xFF)
                ^ ((state >> 8) & 0xFF)
                ^ ((state >> 16) & 0xFF)
                ^ ((state >> 24) & 0xFF)
            )

        buf[i] ^= k
        
    while last >= 0 and buf[last] == 0xFF and last + 1 < len(buf):
        last += 1

        state = (state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF

        if legacy_mode:
            k = state & 0xFF
        else:
            k = (
                (state & 0xFF)
                ^ ((state >> 8) & 0xFF)
                ^ ((state >> 16) & 0xFF)
                ^ ((state >> 24) & 0xFF)
            )

        buf[last] = k

    return bytes(buf)

data = open(sys.argv[1], "rb").read()
decrypted = env_crypt(data[:0x1000], SERIAL)

with open("dec.bin", "wb") as outf:
    outf.write(decrypted)
