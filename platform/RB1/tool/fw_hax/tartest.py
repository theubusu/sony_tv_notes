import tarfile
import io

with tarfile.open("test.tar", "w") as tar:
    data = b"hello from NAND\n"
    info = tarfile.TarInfo("/NAND/hello.txt")
    info.size = len(data)
    tar.addfile(info, io.BytesIO(data))