import sys
import struct
import hashlib
from Crypto.Cipher import AES

KEY = bytes.fromhex("cd3ef441f621b6fa00816e9fe1e9c4e9")
IV  = bytes.fromhex("79bce205052fee4353d9516a3a6b7987")

MAGIC = 0xDF81352E

#setting
UPDATE_ID = 0x0FA30A05A0A5
MODEL = 0x00002100
MAJOR = 0x07b0          #4.600(1967) + 1
MINOR = 0x0000

with open(sys.argv[1], "rb") as inf:
    data = inf.read()
    
out_name = f"{MODEL:08x}_{MAJOR:04x}{MINOR:04x}.bin"
print(f"out_name={out_name}")

folder_name = f"sony_dtv{UPDATE_ID:012X}_{MODEL:08X}"
print(f"folder_name={folder_name}")

with open(out_name, "wb") as outf:
    
    datasize = len(data)
    filesize = datasize + 0x40
    
    hdr = b""
    print(f"[hdr] magic={MAGIC:08x}")
    hdr += struct.pack("<I", MAGIC)
    print(f"[hdr] model={MODEL:08x}")
    hdr += struct.pack("<I", MODEL)
    print(f"[hdr] major={MAJOR:04x}")
    hdr += struct.pack("<I", MAJOR)
    print(f"[hdr] minor={MINOR:04x}")
    hdr += struct.pack("<I", MINOR)
    print(f"[hdr] filesize={filesize}")
    hdr += struct.pack("<I", filesize)
    print(f"[hdr] datasize={datasize}")
    hdr += struct.pack("<I", datasize)
    hdr += b"\x00"*8
    
    #header and data encrypted and hashed together
    encdata = b""
    encdata += hdr
    encdata += data
    
    sha = hashlib.sha1(encdata).digest()
    print(f"sha={sha.hex()}")
    
    sha_hdr = AES.new(KEY, AES.MODE_CBC, iv=IV).encrypt(sha + b"\x00"*12)     #sha header seperately encrypted
    outf.write(sha_hdr)
    
    encdata = AES.new(KEY, AES.MODE_CBC, iv=IV).encrypt(encdata)
    outf.write(encdata)