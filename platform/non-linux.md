# Non-Linux based TVs

Many TVs released mostly in Europe before 2010 use NEC EMMA series CPU, with a custom RTOS running instead of Linux. The app seems to have some references to Nucleus RTOS, so it could be based on that.

## Chassis list(not complete)
### ...
TBD

### 2008
- EG1H, EMMA3SL
- EG1L, EMMA3SL
- EG1W, EMMA3SL
- SE2AG, EMMA2LR

### 2009
- EX2L, EMMA3TL

##
EX2L has the same style of bootloader storage in NAND and similar FTL(`tool/sony_nand_ftl_tool.py`) to AZ1 (EMMA3TL v EMMA3TL2)

The bootloader is just seemingly called "Launcher"

### Launcher platform strings (in EX2L)
```
FIX_00		FIX Chassis (x2000)
FIX1		? same as FIX?
WAX2		2006
FIX2		2007
WAX3		2007
EG1L_L		2008
EG1H		2008
FL1E		2008 XEL-1
EX2L		2009
EG2L		(that is EX2L)
CAMEL		?
POLO		Polo name used in some EG1L - 2008 series tv
SE3			?	(there is a SE2 - 2007, but no SE3?)
SE3SLIM		?
```

The main application is in a format with multiple "Cookie" headers. It can be ZLIB compressed, signed and possibly also encrypted.

The NAND is not encrypted It uses FAT filesystem in the NAND, example for EX2L:
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

## Firmware
The MS firmware for these TVS is in the SPF/SPF2 format.

Older SPF1 files also shipped with a `.ram` application file which actually decrypts and installs it, it seems to use an AES decryption function mapped outside of the application.