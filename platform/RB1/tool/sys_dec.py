import sys

CRYPT_SEED = 0xB9E31AFD

def sony_crypt(data, seed):
    state = seed & 0xFFFFFFFF
    output = bytearray()

    for b in data:
        state = (state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF

        key = (
            (state      ) ^
            (state >>  8) ^
            (state >> 16) ^
            (state >> 24)
        ) & 0xFF

        output.append(b ^ key)

    return bytes(output)
    
outf = open(sys.argv[2], "wb")
with open(sys.argv[1], "rb") as file:
    header = file.read(0x200)
    header = sony_crypt(header, CRYPT_SEED)
    outf.write(header)
    
    data = file.read()
    data = sony_crypt(data, CRYPT_SEED)
    outf.write(data)
