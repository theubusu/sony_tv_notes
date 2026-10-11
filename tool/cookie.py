import struct
import sys
import zlib

with open(sys.argv[1], "rb") as file:
    
    while True:
        magic = file.read(6)
        if magic == b"Cookie":
            type = file.read(2)
            
            
            if type == b"01":       # info
                print("Cookie01")
                
                version = struct.unpack(">I", file.read(4))[0]
                file_type = struct.unpack(">I", file.read(4))[0]
                str_offset = struct.unpack(">H", file.read(2))[0]
                str_end = struct.unpack(">H", file.read(2))[0]
                if str_offset != 0:
                    str_len = str_end - str_offset
                    file_name = file.read(str_len).decode("utf-8").strip("\x00")
                else:
                    file_name = ""
                
                print(f"    version: {version:08x}")
                print(f"    file type: {file_type:08x}")
                print(f"    file name: {file_name}")
                
                
            elif type == b"02":
                print("Cookie02")
                
                file_action = struct.unpack(">I", file.read(4))[0]
                decompressed_size = struct.unpack(">I", file.read(4))[0]
                stored_size = struct.unpack(">I", file.read(4))[0]
                checksum = struct.unpack(">I", file.read(4))[0]
                str_offset = struct.unpack(">H", file.read(2))[0]
                str_end = struct.unpack(">H", file.read(2))[0]
                if str_offset != 0:
                    str_len = str_end - str_offset
                    path = file.read(str_len).decode("utf-8").strip("\x00")
                else:
                    path = ""
                
                print(f"    file action: {file_action:08x}")
                print(f"    decompressed size: {decompressed_size}")
                print(f"    stored size: {stored_size}")
                print(f"    checksum: {checksum:08x}")
                print(f"    path: {path}")
                
            elif type == b"03":
                print("Cookie03")
                
                load_addr = struct.unpack(">I", file.read(4))[0]
                entry_addr = struct.unpack(">I", file.read(4))[0]
                hash = file.read(0x41).decode("utf-8").strip("\x00")    #   Unknown
                unk1 = struct.unpack(">B", file.read(1))[0]             #   Unknown
                unk2 = struct.unpack(">H", file.read(2))[0]             #   Unknown
                
                print(f"    load address: {load_addr:08x}")
                print(f"    entry address: {entry_addr:08x}")
                print(f"    hash: {hash}")
                print(f"    unk1: {unk1:02x}")
                print(f"    unk2: {unk2:04x}")
            
            elif type == b"04":     # padding
                print("Cookie04")
                
                lenght = struct.unpack(">B", file.read(1))[0]
                file.read(lenght)       #discarded
                
                print(f"    lenght: {lenght}")
    
            elif type == b"05":     # signature
                print("Cookie05")
                
                unk1 = struct.unpack(">I", file.read(4))[0]         #   Unknown
                signature = file.read(0x80)
                unk2 = struct.unpack(">I", file.read(4))[0]         #   Unknown
                unk3 = struct.unpack(">H", file.read(2))[0]         #   Unknown
                
                print(f"    unk1: {unk1:08x}")
                print(f"    signature: {signature.hex()[:32]}...")
                print(f"    unk2: {unk2:08x}")
                print(f"    unk3: {unk3:04x}")
                
            else:
                print(f"Unknown Cookie type {type}")
        else:
            # End
            file.seek(file.tell()-6)
            break
    
    print()    
    # do execution
    
    if len(sys.argv)>2:
        
        data = file.read(stored_size)
        print("Decompressing data...")
        try:
            data = zlib.decompress(data)
        except zlib.error as e:
            print(f"Failed to decompress, data is probably encrypted. ({e})")
            exit()
        
        with open(file_name, "wb") as outf:
            outf.write(data)
        print(f"Saved to {file_name}     exec {load_addr:08x}")
        