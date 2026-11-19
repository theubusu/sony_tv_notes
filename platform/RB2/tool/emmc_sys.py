import sys
import struct

BLOCK_SIZE = 512

COMP_NAME = {
    0x00: "DDRInit+Standby",
    0x02: "ABK",
    0x48: "MiniKernel",
    0x60: "Environment",
    0x46: "LogoFW",
}


with open(sys.argv[1], "rb") as file:   
    file.seek(0x8000)
    hdr = file.read(16)
    magic = struct.unpack(">I", hdr[0:4])[0]
    total_blk = struct.unpack(">I", hdr[4:8])[0]
    
    if magic != 0xb4b98a94:
        print(f"Error : Invalid SystemTable Magic")
        exit()
    #total size of system area/fs area start
    print(f"total - blk: {total_blk}, size: {total_blk*BLOCK_SIZE}")    
    
    print(f"{'IDX':<4} {'TYPE':<6} {'NAME':<20} {'BACK':<4} {'VER':<6} {'START':<8} {'LEN':<8} {'OFFSET':<8} {'SIZE':<8}")
    for i in range(31):
        entry = file.read(16)
        type = entry[1]
        version = entry[2]
        start = struct.unpack('>I', entry[4:8])[0]
        len = struct.unpack('>I', entry[8:12])[0]
        
        offset = start*BLOCK_SIZE
        size = len*BLOCK_SIZE
        
        if len == 0xffffffff:
            print(f"{i:<4} invalid")
            continue
        
        print(f"{i:<4} {hex(type & ~1):<6} {COMP_NAME.get(type&~1, '?'):<20} {type & 1:<4} {hex(version):<6} {start:<8} {len:<8} {offset:<8} {size:<8}")