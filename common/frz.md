# FRZ file format
The FRZ file format is used by Sony here in order to store executable binaries.   
It is used for example for the kernel image - `VMLINUX.FRZ`, loaded by the bootloader.   
It is also used for the firmware package on AZ1 and EEGS.   
It's also seen on older sets for some EDID data or other firmware.

FRZ probably refers to the FRoZen state of the application/binary.

Basic FRZ extractor/parser in `tool/frz_new.py`

## Format
The FRZ file is consists of multiple sections, each section starts with a 9 byte header:

## Chunktypes dirty note
`0xf1` - raw data, XORed   
`0xf2` - LZSS compressed, XORed   
`0xf3` - sets entry point, XORed

`0xf4` - raw data, no XOR   
`0xf5` - LZSS compressed, no XOR  
`0xf6` - sets entry point, no XOR   

### new format

`0xf7` - new frz raw chunk, new frz start marker   
`0xf8` - new frz LZSS compressed chunk    
`0xf9` - sets entry point, ends file    