import struct
import sys

with open(sys.argv[1], "rb") as file:
    
    magic = file.read(4)
    if magic != b"Env\x00":
        print("error: magic is not corrrect")
        exit()

    size = struct.unpack(">I", file.read(4))[0]
    num = struct.unpack(">I", file.read(4))[0]
    sum = struct.unpack(">I", file.read(4))[0]
    
    print(f"[Env] size={size}, num={num}, sum={hex(sum)}")
    
    for i in range(num):
        marker = file.read(1)
        size = struct.unpack(">I", file.read(4))[0]
        
        name = b""
        while True:
            b = file.read(1)
            if b == b"\x00":
                break
            name += b
        name = name.decode("utf-8")
        
        data = file.read(size)
        
        print(f"[{i}] {name}, marker={marker}, size={size}: {data[:40]}...")