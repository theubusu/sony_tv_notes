import sys

#
#   AEP - KDL-40W4500
#   1x64MB = 64MB
#
def process_aep(nand, outfile):
    NAND_DATA_SIZE = 512
    NAND_OOB_SIZE = 16
    
    INTR_BLOCK_SIZE = 16384
    INTR_TOTAL_BLOCKS = 1024
    
    for i in range(INTR_TOTAL_BLOCKS):
        block = bytearray()
   
        # read block 
        for bi in range(INTR_BLOCK_SIZE // NAND_DATA_SIZE):
            data = nand.read(NAND_DATA_SIZE)
            oob = nand.read(NAND_OOB_SIZE)
            block += data
        
            # use LAST oob of block
            if bi == ((INTR_BLOCK_SIZE // NAND_DATA_SIZE) -1):
                counter = (oob[2] << 8) | oob[3]
            
        print(f"{i} -> {counter}")                  
        if not counter > INTR_TOTAL_BLOCKS:
            outfile.seek(counter * INTR_BLOCK_SIZE)
            outfile.write(block)
        
#
#   EG2L - KDL-40V5500
#   2x64MB = 128MB
#
def process_eg2l(nand1, nand2, outfile):
    NAND_DATA_SIZE = 512
    NAND_OOB_SIZE = 16
    
    INTR_BLOCK_SIZE = 16384
    INTR_TOTAL_BLOCKS = 8192

    def process_nand(nand_i, nand):
        for i in range(INTR_TOTAL_BLOCKS // 2):   
            block = bytearray()
   
            # read block 
            for bi in range(INTR_BLOCK_SIZE // NAND_DATA_SIZE):
                data = nand.read(NAND_DATA_SIZE)
                oob = nand.read(NAND_OOB_SIZE)
        
                block += data
        
                # use LAST oob of block
                if bi == ((INTR_BLOCK_SIZE // NAND_DATA_SIZE) -1):
                    counter = (oob[10] << 8) | oob[11]
            
            print(f"[NAND{nand_i}] {i} -> {counter}")        
            
            if not counter > INTR_TOTAL_BLOCKS:
                outfile.seek(counter * INTR_BLOCK_SIZE)
                outfile.write(block)
            
    process_nand(1, nand1)
    process_nand(2, nand2)
    
#
#   EMMA - KDL-40NX805
#   2x64MB = 128MB
#
def process_emma(nand1, nand2, outfile):
    NAND_DATA_SIZE = 512
    NAND_OOB_SIZE = 16

    INTR_BLOCK_SIZE = 32768
    INTR_TOTAL_BLOCKS = 4096
    
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
                counter = nand1_oob[9] | (nand2_oob[9] << 8)
      
        print(f"{i} -> {counter}")
    
        if not counter > INTR_TOTAL_BLOCKS: #0xFFFF probably means block not used
            outfile.seek(counter * INTR_BLOCK_SIZE)
            outfile.write(block)
    
#
#   EEGS
#   2x64MB = 128MB
#      
def process_eegs(nand1, nand2, outfile):
    NAND_DATA_SIZE = 512
    NAND_OOB_SIZE = 16

    INTR_BLOCK_SIZE = 32768
    INTR_TOTAL_BLOCKS = 4096
   
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
                counter = nand2_oob[4] | (nand1_oob[4] << 8)  
            
        #unswap
        for si in range(0, len(block), 4):
            block[si:si+4] = block[si:si+4][::-1]
      
        print(f"{i} -> {counter}")
    
        if not counter > INTR_TOTAL_BLOCKS: #0xFFFF probably means block not used
            outfile.seek(counter * INTR_BLOCK_SIZE)
            outfile.write(block)

#
#   
#
#               
if len(sys.argv) < 4:
    print("SONY TV NAND FTL tool")
    print("usage: x <mode> <out file> <NAND1> <NAND2(optional)>")
    print("modes:")
    print("AEP - 1xNAND")
    print("EG2L - 2xNAND")
    print("EMMA - 2xNAND")
    print("EEGS - 2xNAND")
    exit()

mode = sys.argv[1].lower()
outfile = open(sys.argv[2], "wb")
if mode == "aep":
    process_aep(open(sys.argv[3], "rb"), outfile)
elif mode == "eg2l":
    process_eg2l(open(sys.argv[3], "rb"), open(sys.argv[4], "rb"), outfile)
elif mode == "emma":
    process_emma(open(sys.argv[3], "rb"), open(sys.argv[4], "rb"), outfile)
elif mode == "eegs":
    process_eegs(open(sys.argv[3], "rb"), open(sys.argv[4], "rb"), outfile)
else:
    print("unknown mode!")
    exit()

