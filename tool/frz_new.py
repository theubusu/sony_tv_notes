import sys
import os
import struct
from lzs import lzs_decompress 

IS_NEW_TYPE = False
    
with open(sys.argv[1], "rb") as file:
    frz = file.read()
    
output_folder = sys.argv[2]
if not os.path.exists(output_folder):
    os.makedirs(output_folder)    
    
i = 0
while True:
    if len(frz) < 9:
        break
    sec_hdr = frz[:9]
    frz = frz[9:]
        
    flag, size, load_addr = struct.unpack(">BII", sec_hdr)
    print(f"[{i}] flag={flag:x}, size={size}, load_addr={load_addr:x}")
    #print(f"    {bin(flag)}")
    
    decomp = None
    if IS_NEW_TYPE:             # new type stores the COMPRESSED size in header. idk how it determines whether a section is compressed in new
        data = frz[:size]
        frz = frz[size:]
        
        decomp, _ = lzs_decompress(data)  
        print(f"    decomp {len(decomp)}")
 
    else:               # old type stores the UNCOMPRESSED size in header (if section compressed)
        if (flag & (1 << 0)) != 0:  #compressed
            decomp, consumed = lzs_decompress(frz, size)
            print(f"    consumed {consumed}")
            print(f"    decomp {len(decomp)}")
            
            data = frz[:consumed]
            frz = frz[consumed:]
        else:   #uncompressed
            data = frz[:size]
            frz = frz[size:]
           
    # checksum of stored data follows      
    checksum = struct.unpack(">I", frz[:4])[0]
    frz = frz[4:]

    calc = sum(sec_hdr[1:] + data) & 0xFFFFFFFF         #simple Checksum32
    print(f"    chk. exp={hex(checksum)}, calc={hex(calc)}\n")
    assert checksum == calc
    
    open(f"{output_folder}/{i}_{load_addr:x}.bin", "wb").write(data)
    if decomp:
        open(f"{output_folder}/{i}_{load_addr:x}.dec", "wb").write(decomp)
    
    i+=1