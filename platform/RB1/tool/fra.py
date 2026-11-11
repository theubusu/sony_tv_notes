import struct
import sys
import zlib
import os
from decsrv import decrypt_data
from hexdump import hexdump

fradec = False    #mimic /dev/fradec (skip first section and merge rest to one stream)
dodecrypt = True  
if len(sys.argv) >= 3:
    outd = sys.argv[2]
    if "-f" in sys.argv:
        fradec = True
        outf = open(outd, "wb")
    else:
        if not os.path.exists(outd):
            os.makedirs(outd)
            pass
        
    if "-d" in sys.argv:
        dodecrypt = False
else:
    print(f"FRA file tool")
    print(f"usage: {sys.argv[0]} <INPUT FILE> <OUTPUT> [OPTIONS]")
    print(f"Options:")
    print(f"-f : Mimic /dev/fradec - combine all sections except the first into one output file.")
    print(f"-d : Use a already decrypted fra file, No decryption will be done.")
    exit()
            
with open(sys.argv[1], "rb") as file:
    file_header = file.read(0x80)

    if file_header[0:16] != b"\xf4\xf1\x82\x93\x22\x9e\xe9\x54\xa9\x9d\x79\xd5\x75\xdb\x6c\x60":
        print("[-] Invalid MagicCode")
        exit()
        
    tmp_buf_addr = struct.unpack(">I", file_header[16:20])[0]
    file_header_size = struct.unpack(">I", file_header[20:24])[0]
    section_header_size = struct.unpack(">I", file_header[24:28])[0]
    payload_size = struct.unpack(">I", file_header[28:32])[0]
    section_header = struct.unpack(">I", file_header[32:36])[0]
    security_header_size = struct.unpack(">I", file_header[36:40])[0]  
    section_header_mac = file_header[48:64]
    initial_vector = file_header[64:80]
    release_key = file_header[80:96]
    package_mac = file_header[96:112]
    
    print(f"[i] SectionHeaderSize: {section_header_size}\n[i] PayloadSize: {payload_size}\n[i] SecurityHeaderSize: {security_header_size}")
    
    #skip security header
    security_header = file.read(security_header_size)
    #if security_header_size != 0:
    #    security_header = decrypt_data(security_header, release_key, initial_vector)
    #    print(f"[i] Security header:")
    #    hexdump(security_header)
    
    #read section header(s)
    section_headers = file.read(section_header_size)
    if dodecrypt:
        section_headers = decrypt_data(section_headers, release_key, initial_vector)
    
    section_block_header = section_headers[:0x80]
    section_num = struct.unpack(">I", section_block_header[0:4])[0]
    entry_point = struct.unpack(">I", section_block_header[4:8])[0]
    file_type = struct.unpack(">I", section_block_header[8:12])[0]
    build_time = struct.unpack(">I", section_block_header[12:16])[0]
    #follows some metadata not important
    
    print(f"[i] SectionNum: {section_num}")
    
    for i in range(section_num):
        print(f"Section [{i}]")
        section_hdr = section_headers[0x80 + (i*0x80): 0x80 + ((i+1)*0x80)]
        #hexdump(section_hdr)
        
        payload_offset = struct.unpack(">I", section_hdr[0:4])[0]
        payload_size = struct.unpack(">I", section_hdr[4:8])[0]
        records = struct.unpack(">I", section_hdr[8:12])[0]
        section_type = struct.unpack(">I", section_hdr[12:16])[0]
        memory_address = struct.unpack(">I", section_hdr[16:20])[0]
        memory_size = struct.unpack(">I", section_hdr[20:24])[0]
        area_size = struct.unpack(">I", section_hdr[24:28])[0]
        sub_entry_point = struct.unpack(">I", section_hdr[28:32])[0]
        section_mac = section_hdr[48:64]
        section_initial_vector = section_hdr[64:80]
        reserved2 = section_hdr[80:96]
        
        print(f"    PayloadOffset: {payload_offset}\n    PayloadSize: {payload_size}\n    Records: {records}\n    Memory address: {hex(memory_address)}\n    Memory size: {memory_size}\n    Area size: {area_size}")
        
        #assert file.tell() == file_header_size + section_header_size + security_header_size + payload_offset
        payload = file.read(payload_size)
        if dodecrypt:
            payload = decrypt_data(payload, release_key, section_initial_vector)
        
        #decompress (done on hw side)
        if records == 1:
            payload = zlib.decompress(payload, wbits=-15)
        
        
        if fradec:
            if i != 0:
                outf.write(payload)
        else:
            open(f"{outd}/{i}.bin", "wb").write(payload)