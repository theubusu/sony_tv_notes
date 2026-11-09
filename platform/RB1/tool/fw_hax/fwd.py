import sys
import struct
import hashlib
from Crypto.Cipher import AES

from hexdump import hexdump

KEY = bytes.fromhex("cd3ef441f621b6fa00816e9fe1e9c4e9")
IV  = bytes.fromhex("79bce205052fee4353d9516a3a6b7987")

with open(sys.argv[1], "rb") as file:
    sha_hdr = file.read(32)
    sha_hdr = AES.new(KEY, AES.MODE_CBC, iv=IV).decrypt(sha_hdr)
    sha_exp = sha_hdr[:20]
    print(f"[i] Expected SHA digest: {sha_exp.hex()}")
    
    aes = AES.new(KEY, AES.MODE_CBC, iv=IV)
    sha = hashlib.sha1()
    
    hdr = file.read(32)
    hdr = aes.decrypt(hdr)
    sha.update(hdr)

    magic = struct.unpack("<I", hdr[0:4])[0]
    model = struct.unpack("<I", hdr[4:8])[0]
    major = struct.unpack("<I", hdr[8:12])[0]
    minor = struct.unpack("<I", hdr[12:16])[0]
    filesize = struct.unpack("<I", hdr[16:20])[0]
    datasize = struct.unpack("<I", hdr[20:24])[0]
    
    if magic != 0xDF81352E:
        print(f"[!] Error: invalid magic ({hex(magic)})")
        exit()
        
    print(f"[i] model={model:08x}, major: {major:04x}, minor:{minor:04x}")
    print(f"[i] filesize={filesize}, datasize={datasize}")
    
    data = file.read(filesize - 0x40)
    if len(data) != datasize:
        print(f"[!] Error: invalid data size")
        exit()
    data = aes.decrypt(data)
    sha.update(data)
    
    sha_calc = sha.digest()
    print(f"[i] Calculated SHA digest: {sha_calc.hex()}")
    
    if sha_calc != sha_exp:
        print(f"[!] Error: SHA verification failed")
        exit()
    else:
        print(f"[+] SHA verification OK")
        
    open("out.tar", "wb").write(data)