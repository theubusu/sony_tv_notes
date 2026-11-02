## Make decrypted FRA file

import struct
import sys
from decsrv import decrypt_data
from hexdump import hexdump
    
OUT_PATH = sys.argv[1] + ".dec"    
    
outf = open(OUT_PATH, "wb")
    
with open(sys.argv[1], "rb") as file:
    file_header = file.read(0x80)

    if file_header[0:16] != b"\xf4\xf1\x82\x93\x22\x9e\xe9\x54\xa9\x9d\x79\xd5\x75\xdb\x6c\x60":
        print("[-] Invalid MagicCode")
        exit()
        
    section_header_size = struct.unpack(">I", file_header[24:28])[0]
    security_header_size = struct.unpack(">I", file_header[36:40])[0]  
    initial_vector = file_header[64:80]
    release_key = file_header[80:96]
    
    print(f"[i] SectionHeaderSize: {section_header_size}\n[i] SecurityHeaderSize: {security_header_size}")
    
    outf.write(file_header)
    
    #skip security header
    security_header = file.read(security_header_size)
    if security_header_size != 0:
        security_header = decrypt_data(security_header, release_key, initial_vector)
        print(f"[i] Security header:")
        hexdump(security_header)
        outf.write(security_header)
    
    #read section header(s)
    section_headers = file.read(section_header_size)
    section_headers = decrypt_data(section_headers, release_key, initial_vector)
    
    outf.write(section_headers)
    
    section_block_header = section_headers[:0x80]
    section_num = struct.unpack(">I", section_block_header[0:4])[0]    
    print(f"[i] SectionNum: {section_num}")
    
    for i in range(section_num):
        print(f"Section [{i}]")
        section_hdr = section_headers[0x80 + (i*0x80): 0x80 + ((i+1)*0x80)]
        payload_size = struct.unpack(">I", section_hdr[4:8])[0]
        section_initial_vector = section_hdr[64:80]
        
        print(f"    PayloadSize: {payload_size}")

        payload = file.read(payload_size)
        payload = decrypt_data(payload, release_key, section_initial_vector)
        
        assert len(payload) == payload_size
        outf.write(payload)
        
        