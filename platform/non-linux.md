# Non-Linux based TVs

Many TVs released mostly in Europe before 2010 (see launcher platforms) use NEC EMMA series CPU, with a custom RTOS running instead of Linux. The app seems to have some references to Nucleus RTOS, so it could be based on that.

## NAND
The NAND is not encrypted, but uses one of FTL systems. (see `tool/sony_nand_ftl_tool.py`) It contains one main FAT16 partition with the system files.

### Contents of NAND for EX2L
|path     | desc      |
|-----|---------|
|APP.A| Main application image |
|APP.B| Backup application image |
|CMW | Unknown |
|emulate_eep.0 | has `0000.EMU` emulated eeprom 0 |
|emulate_eep.1 | has `0000.EMU` emulated eeprom 1 |
|INSTALL    | package installation info |
|LAUNCHER   | Application launcher information |
|MDW    | Saved channel info? |
|NVM    | empty |
|OAD    | OAD update data |
|OSIM   | i-Manual data |
|PQC    | PQ data |
|RESOURCE| empty |
|RFS    | has `timers.dat`, purpose unknown |
|SFS    | has strings and font in `RES` folder |
|STATE  | has file `emma_update_check.txt`, purpose unknown |
|__SYSTEM | X2 Data |
|MEMSTICK.IND   | empty file |

The later TV's have support for X2 system and also XML widgets.

## Bootloader
The bootloader is called "Launcher" and it loads the main application file from the FAT filesystem on NAND

```
(c) Copyright 2008 Sony Corporation

Launcher Version: 40
Launcher Build Id: RELEASE
Launcher MSE Release: 127
Launcher MSE Version: MSE2B_INT_BAS_127
Launcher MSE Config: eg2l_dvt
Launcher Platform: EX2L (256MB DDR)
```

### Launcher platform strings (in EX2L, so latest(?))
```
fix/fix_00		FIX Chassis (x2000) 2006
FIX1			? same as FIX?
FIX2			2006
WAX2			2006
WAX3			2007
EX1				2008
EG1L_L			2008, EMMA3SL
EG1H			2008, EMMA3SL
FL1E			2008 (XEL-1 Europe), EMMA3SL
POLO			Polo=EG1L 2008, EMMA3SL
Camel			?
SE3				?
se3slim			?
eg2l/EX2L		2009, EMMA3TL

emma3tl_eval	Eval board
emma3sl_eval	Eval board
```

The main application is in a format with multiple "Cookie" headers. It can be ZLIB compressed, signed and also encrypted. See `tool/cookie.py`

## Firmware
The MS firmware for these TVS is in the SPF/SPF2 format.

SPF files also ship with a `.ram` file (Application in the "Cookie" format) which is loaded by the bootloader and actually performs the installation. 

SFP1 (before 2009) files are decrypted using a hardcoded AES key in AES256-CBC-CTS mode, where the first 0x10 bytes of the file is the IV and can be decrypted(implemented in [unixtract](https://github.com/theubusu/unixtract/tree/main/src/formats/spf1)). They are just a compressed and encrypted TAR archive with a simple header.

SPF2 (2009(+?)) files are encrypted using some sort of hardware AES, and cannot be decrypted as of now. They also most likely contain a TAR archive inside. Those are also shipped as USB files with name `FIRMWARE.UPD`, which has additional header, but is still an SPF2 file.