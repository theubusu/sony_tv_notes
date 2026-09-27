import sys

NAND_DATA_SIZE = 512
NAND_OOB_SIZE = 16

INTR_BLOCK_SIZE = 32768
INTR_TOTAL_BLOCKS = 4096

if len(sys.argv) < 4:
    print("usage: emma_ftl.py <NAND1 file> <NAND2 file> <output file> <eegs mode>")
    exit()

if len(sys.argv) == 5:
    EEGS_MODE = True
else:
    EEGS_MODE = False

nand1 = open(sys.argv[1], "rb")
nand2 = open(sys.argv[2], "rb")
outfile = open(sys.argv[3], "wb")

for i in range(INTR_TOTAL_BLOCKS):
    
    block = bytearray()
   
    # read block 
    for bi in range(INTR_BLOCK_SIZE // NAND_DATA_SIZE//2):
     
        nand1_data = bytearray(nand1.read(NAND_DATA_SIZE))
        nand1_oob = nand1.read(NAND_OOB_SIZE)
        
        nand2_data = bytearray(nand2.read(NAND_DATA_SIZE))
        nand2_oob = nand2.read(NAND_OOB_SIZE)
        
        #deintr
        for ni in range(NAND_DATA_SIZE):
            block.append(nand2_data[ni])
            block.append(nand1_data[ni])
        
        # use first oob of block
        if bi == 0:
            if EEGS_MODE:
                counter = nand2_oob[4] | (nand1_oob[4] << 8)              
            else:
                counter = nand1_oob[9] | (nand2_oob[9] << 8)
                
    #unswap
    if EEGS_MODE:
        for si in range(0, len(block), 4):
            block[si:si+4] = block[si:si+4][::-1]
      
    print(f"phys {i} -> log {counter}")
    
    if not counter > INTR_TOTAL_BLOCKS: #0xFFFF probably means block not used
        outfile.seek(counter * INTR_BLOCK_SIZE)
        outfile.write(block)
            
    #outfile.write(block)
           