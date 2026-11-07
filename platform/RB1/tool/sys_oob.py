import sys
from hexdump import hexdump

BLOCK_SIZE = 262144
NAND_TOTAL_BLOCK = 4096
PAGE_SIZE = 4096
NAND_TOTAL_PAGE = 262144
OOB_SIZE = 224

##
DBG = False
##
def dprint(s):
    if DBG:
        print(s)

file = open(sys.argv[1], "rb")
SYSTEM_TABLE = []

for bi in range(NAND_TOTAL_BLOCK):
    dprint(f"\n[Block {bi}]")
    
    set_param = None
    
    #for each block, read BLOCK_SIZE//PAGE_SIZE pages
    for i in range(BLOCK_SIZE//PAGE_SIZE):
        oob = file.read(OOB_SIZE)
        
        if bi == 0:      #block 0= special system parameters (+fixed env) - skip
            continue
        
        param = oob[8:18]
        if DBG:
            hexdump(param)
    
        chunk_count = param[1]
        unk2 = param[2]
        chunk_index = param[3]
        magic = param[4:7]
        type_copy = param[8]
        version = param[9]
    
        if magic == b"\xff\xff\xff":
            dprint(f"[{i}]   Reserved/unused")
            continue
    
        if magic != b"\xF1\xD6\x5B":
            dprint(f"[{i}]   Unexpected magic")
            break
        
        dprint(f"[{i}]   chunk_count={chunk_count}, chunk_index={chunk_index}, type_copy={type_copy} (type={hex(type_copy & ~1)}, copy={type_copy & 1}), version={version}")
        
        #set param on 0blk
        if i == 0:
            set_param = param
        else: #verify param of 0 blk
            if set_param != param:
                print(f"[{i}]   Err: set param mismatched!")
                exit()
                        
    else:
        #success block
        if set_param:       #param was set, block was used
            #packing of systemtable
            entry = ((set_param[8] << 24) | (set_param[9] << 16) | (set_param[2] << 8) | ((set_param[1] & 0xF) << 4) | (set_param[3] & 0xF))
            SYSTEM_TABLE.append(entry)
        elif bi == 0:
            SYSTEM_TABLE.append(0xffffffff)     # reserved blk
        else:
            SYSTEM_TABLE.append(0x00000000)      #unused blk
        continue
    break
    

print(f"\n[STOP] FileSystemStartBlock={bi} ?")
FileSystemStartBlock = bi

print(f"SYSTEM_TABLE:")
for si, s in enumerate(SYSTEM_TABLE):
    print(f"[{si:04d}] = 0x{s:08x}")
    
    
## now parse system table to component map
COMP_NAME = {
    0x00: "DDRInit+Standby",
    0x02: "ABK",
    0x48: "MiniKernel",
    0x60: "Environment",
    0x46: "LogoFW",
}

comps, counts, versions = {}, {}, {}
for bi, e in enumerate(SYSTEM_TABLE):
    if e == 0x00000000 or e == 0xFFFFFFFF:
        continue
    type_copy = e >> 24
    type, copy = type_copy & ~1, type_copy & 1
    version = (e >> 16) & 0xFF
    count = (e >> 4) & 0xF
    index = e & 0xF
    
    comps.setdefault(type, {}).setdefault(copy, {})[index] = bi    
    versions.setdefault(type, {}).setdefault(copy, version)
    counts[type] = count

for type in comps:
    print(f"\n0x{type:02x} - {COMP_NAME.get(type, '?'):<20} size: {counts[type]} blk ({counts[type]*BLOCK_SIZE})")
    for copy in comps[type]:
        chunks = comps[type][copy]
        blocks = [chunks[i] for i in chunks]         
        print(f"\t{copy}: {blocks[0]:<3} (0x{blocks[0]*BLOCK_SIZE:06X})   version=0x{versions[type][copy]:x}")