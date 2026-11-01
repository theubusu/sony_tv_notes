import sys
import struct
import hexdump
import os

outd = None
if len(sys.argv) == 3:
    outd = sys.argv[2]
    if not os.path.exists(outd):
        os.makedirs(outd)

with open(sys.argv[1], "rb") as file:
    
    file_header = file.read(0x100)
    print(f"== File header ==")
    print(f"Size: {struct.unpack(">I", file_header[0:4])[0]}")
    print(f"Sum: {struct.unpack(">I", file_header[4:8])[0]:08x}")
    print(f"Mode: {struct.unpack(">I", file_header[8:12])[0]:04x}")
    print(f"ModelIDMask: {struct.unpack(">I", file_header[12:16])[0]:08x}")
    print(f"ModelIDCompare[0]: {struct.unpack(">I", file_header[16:20])[0]:08x}")
    print(f"SetName: {file_header[0x4c:0x5c].decode("utf-8").strip("\x00")}")
    print(f"StartVersion: {file_header[0x5c:0x6c].decode("utf-8").strip("\x00")}")
    print(f"EndVersion: {file_header[0x6c:0x7c].decode("utf-8").strip("\x00")}")
    
    i = 0
    while True:
        h_size = struct.unpack(">I", file.read(4))[0]
        if h_size == 0:
            break
        file.seek(file.tell()-4)
        object_header = file.read(h_size)
        #hexdump.hexdump(object_header)
        
        print(f"[{i}]")
        print(f"    HSize: {h_size}")
        f_size = struct.unpack(">I", object_header[4:8])[0]
        print(f"    FSize: {f_size}")
        print(f"    ModelID: {struct.unpack(">I", object_header[8:12])[0]:08x}")
        print(f"    ModelIDMaskTrialLevel: {struct.unpack(">I", object_header[0x48:0x48+4])[0]:08x}")
        src_file_name_size = struct.unpack(">I", object_header[0x4c:0x4c+4])[0]
        print(f"    SrcFileNameSize: {src_file_name_size}")
        mode = struct.unpack(">H", object_header[0x50:0x52])[0]
        print(f"    Mode: {mode}")
        type = struct.unpack(">H", object_header[0x52:0x54])[0]
        print(f"    Type: {hex(type)}")
        uid = struct.unpack(">H", object_header[0x54:0x56])[0]
        print(f"    UID: {uid}")
        dev = struct.unpack(">H", object_header[0x56:0x58])[0]
        print(f"    Dev: {uid}")
        
        year, month, day, hour, minute, second = struct.unpack(">6H", object_header[0x58:0x64])
        print(f"    {year}/{month}/{day} {hour:02d}:{minute:02d}:{second:02d}")

        data = file.read(f_size)
        ##dbg
        #if len(data) != 0 and outd:
        #    with open(f"{outd}/_{i}.bin", "wb") as outf:
        #        outf.write(data)
            
        
        if type >= 0 and type <= 6:
            print(f"    => ADD")
            
            if src_file_name_size != 0:
                dst_file_name = object_header[0x64:-src_file_name_size].decode("utf-8").strip("\x00")
            else:
                dst_file_name = object_header[0x64:].decode("utf-8").strip("\x00")
            print(f"    dst_file_name: {dst_file_name}")
            
            if src_file_name_size != 0:
                src_file_name = object_header[-src_file_name_size:].decode("utf-8").strip("\x00")
            else:
                src_file_name = ""
            
            print(f"    src_file_name: {src_file_name}")
            
            if type == 0:
                print(f"    file")
                if outd:
                    if src_file_name == "":
                        outpath = os.path.join(outd, dst_file_name)
                    else:
                        outpath = os.path.join(outd, src_file_name)
                
                
                    with open(outpath, "wb") as outf:
                        outf.write(data)
                    
                    
            elif type == 1:
                print(f"    symlink")      
            elif type == 6:
                print(f"    directory") 
                if outd:
                    if not os.path.exists(os.path.join(outd, dst_file_name)):
                        os.makedirs(os.path.join(outd, dst_file_name))
            else:
                print(f"    not supported")
            
        elif type == 0x10:
            print(f"    => DELETE")
            
        elif type == 0x20:
            print(f"    => SET ENV")
            
        elif type == 0x21:
            print(f"    => UNSET ENV")
            env = object_header[0x64:].decode("utf-8").strip("\x00")
            print(f"    unset {env}")
            
        elif type == 0x40:
            print(f"    => BDI")
            
        elif type == 0x41:
            print(f"    => MERGE")
            print(f"    [extract_type_merge] currently merge is not supported")
            
        elif type == 0x50:
            print(f"    => FORMAT")
            print(f"    [extract_type_format] format is skipped in UserLand fradec")
            
        elif type == 0x60:
            print(f"    => PANELID")
            
        ## not in UserLand fradec
        elif type >= 0x70 and type < 0x7f:
            
            if type == 0x70:
                t_str = "DDRInit"
            elif type == 0x71:
                t_str = "Standby"
            elif type == 0x72:
                t_str = "ABK"
            elif type == 0x73:
                t_str = "LogoFW"
            elif type == 0x74:
                t_str = "MiniKernel"
            else:
                t_str = "unknown"
                
            print(f"    => SYS {t_str}")
            if outd:
                if not os.path.exists(os.path.join(outd, "_sys")):
                    os.makedirs(os.path.join(outd, "_sys"))
                
                with open(os.path.join(outd, "_sys", f"{i}_{t_str}.bin"), "wb") as outf:
                    outf.write(data)
            
        else:
            print(f"    => UNKNOWN type")

        #break
        i += 1