# FRZ file format
The FRZ file format is used by Sony here in order to store executable binaries.   
It is used for example for the kernel image - `VMLINUX.FRZ`, loaded by the bootloader.   
It is also used for the firmware package on AZ1 and EEGS.   
It's also seen on older sets for some EDID data or other firmware.

FRZ probably refers to the FRoZen state of the application/binary.

Basic FRZ extractor/parser in `tool/frz_new.py`

## Format
The FRZ file is consists of multiple sections, each section starts with a 9 byte header: