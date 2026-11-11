import sys
import struct
import hashlib
from Crypto.Cipher import AES

# AZ2/AZ3
KEY_BE = bytes.fromhex("41f43ecdfab621f69f6e8100e9c4e9e1")
IV_BE  = bytes.fromhex("05e2bc7943ee2f056a51d95387796b3a")

# RB1/RB2
KEY_LE = bytes.fromhex("cd3ef441f621b6fa00816e9fe1e9c4e9")
IV_LE  = bytes.fromhex("79bce205052fee4353d9516a3a6b7987")

MAGIC = 0xDF81352E

with open(sys.argv[1], "rb") as file:
    ###### detect
    file.seek(0x20)
    hdr = file.read(32)
    dec = AES.new(KEY_BE, AES.MODE_CBC, iv=IV_BE).decrypt(hdr)
    if struct.unpack(">I", dec[0:4])[0] == MAGIC:
        print(f"[+] BE detected (AZ2/AZ3)")
        key, iv, endian = KEY_BE, IV_BE, ">"
    else:
        dec = AES.new(KEY_LE, AES.MODE_CBC, iv=IV_LE).decrypt(hdr)
        if struct.unpack("<I", dec[0:4])[0] == MAGIC:
            print(f"[+] LE detected (RB1/RB2)")
            key, iv, endian = KEY_LE, IV_LE, "<"
        else:
            print("[!] Failed to detect, file not compatible?")
            exit()
    file.seek(0)
    ###### reset
    
    sha_hdr = file.read(32)
    sha_hdr = AES.new(key, AES.MODE_CBC, iv=iv).decrypt(sha_hdr)
    sha_exp = sha_hdr[:20]
    print(f"[i] Expected SHA digest: {sha_exp.hex()}")
    
    aes = AES.new(key, AES.MODE_CBC, iv=iv)
    sha = hashlib.sha1()
    
    hdr = file.read(32)
    hdr = aes.decrypt(hdr)
    sha.update(hdr)

    magic = struct.unpack(f"{endian}I", hdr[0:4])[0]
    model = struct.unpack(f"{endian}I", hdr[4:8])[0]
    major = struct.unpack(f"{endian}I", hdr[8:12])[0]
    minor = struct.unpack(f"{endian}I", hdr[12:16])[0]
    filesize = struct.unpack(f"{endian}I", hdr[16:20])[0]
    datasize = struct.unpack(f"{endian}I", hdr[20:24])[0]
    
    if magic != MAGIC:
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
        
    open(f"{sys.argv[1]}.dec", "wb").write(data)