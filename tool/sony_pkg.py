import struct
import sys
import os

if len(sys.argv) > 2:
    if sys.argv[2] == "b":
        endian = ">"
    elif sys.argv[2] == "l":
        endian = "<"
    else:
        print("not valid specified endian value (b or l)")
        exit()
else:
    print("not specfied endian vaule (b or l)")
    exit()

if len(sys.argv) > 3:
    save_dir = sys.argv[3]
else:
    save_dir = None
    
with open(sys.argv[1], "rb") as file:
    ## header
    file.read(2)        #unknown, always 0010?
    header_size = struct.unpack(f'{endian}B', file.read(1))[0]
    firmware_name = file.read(48).decode('utf-8').strip('\x00')
    file.read(1) #empty
    section_count = struct.unpack(f'{endian}B', file.read(1))[0]
    file.read(9) #empty
    
    print(f"[hdr] header_size={header_size}, firmware_name={firmware_name}, section_count={section_count}")
    
    sections = []
    for i in range(section_count):
        section_size = struct.unpack(f'{endian}L', file.read(4))[0]      
        sections.append(section_size)
    
    print(f"[hdr] sections={sections}")
    
    assert file.tell() == header_size
    
    ## data
    for i, section in enumerate(sections):
        #each section also seems to start with some 16 byte heading
        data = file.read(section)
 
        if save_dir:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            with open(os.path.join(save_dir, str(i) + ".bin"), "wb") as out:
                out.write(data)
            print(f"[+] saved section {i}")
            
    ## footer
    footer = file.read(0x44)
    
    print(f"[foot] sha1={footer[:20].hex()}") #calculated from 0 to size-0x44
    
    