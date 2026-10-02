# SF1EG/MARS platform (2004)

This is a Japan only platform/chassis used in  most likely:
- KDE-P37/42/50HVX
- KDL-L26/32/40HVX

In many places it is reffered to as "MARS":
- `MARS_KDE-PxxHVX_1211_V0023_D2.100T_F.frz`
- `*   File Name   : $File: //mars/SF1EG/mp/12th/eegs/app-src/Gui/DgEpg/DgEpg.xml $`
- `/root/mars/platform/build`
- `$Id: //mars/SF1EG/emma/platform/utils/busybox/vi.c#1 $`

But i think SF1EG is the actual Chassis name, which is the naming i want to use.

## SoC
- NEC EMMA2HL (UPD61160F1) MIPS [ref](https://www.eetimes.com/trio-of-emma-chips-for-high-definition-tv/)
- 4x32M SDRAM = 128MB

## NAND/NOR
- NOR: 29LV200TC 256KB, contains the ABK Monitor/bootloader
- NAND: 2xTC58DVM92A1TGI0 64MB = 128MB

NAND has interleaved and FTL setup, see `tool/emma_ftl.py` (with EEGS mode)

### Notable files in NAND:
The root partition is a "UVFAT16"

| name          | purpose |
|---------------|---------|
|`cramfsimage.sony`| Cramfs image of `/sony`|
|`cramfsimage.fixed`| Cramfs image of `/fixed`|
|`cramfsimage.eg_sony`| Cramfs image of `/eg/sony` Files for the EEGS system.|
|`cramfsimage.eg_fixed`| Cramfs image of `/eg/fixed` Files for the EEGS system.|
|`/bin/vmlinux.frz`| Linux kernel image|

## EE/GS
The platform has a EE(Emotion Engine) and GS(Graphics Synthesiser) from PS2 chips on a seperate board, they are used to display the XMB OSD. It communicates with the main board and recieves the firmware and program from it using an FPGA.

## Kernel
`Linux version 2.4.17_mvl21 (root@driverRHL732004) (gcc version 2.95.3 20010315 (release/MontaVista)) #1 Wed Sep 20 09:19:52 GMT 2006`

## Bootloader
The NOR flash contains the ABK Monitor/bootloader, version `M1.202C` from Aug 17 2004 20:13:06

### Environment
Encrypted environment is stored at 0x3A000 in the NOR, size 0x1000. It is decrypted with the `serial` value, which is stored at 0x3D000. See script `tool/dec_env.py`.   
It stores values: `reboot`, `wdt`, `message`, `home`, `password`, `autoboot`, `boot`, `ilink_modelname`, `ilink_modelid`, `set_serial`, `setname`, `module`

There is also another blob of data encrypted the same way at 0x3C000, it has the values of `macaddr` and `ilinkkey`, and some other unknown data.

## Notes
- This TV does not seem to have any way to update from memorystick/USB.
- UI seems to be rendered at 784x442
- in `/eg/sony/xml/SetupGPLEx4.xml` - cool credits file: https://gist.github.com/uyjulian/88d733d090e6ed071ee1dca60a7fc14e. Makes me wonder if it can be activated from TV menu.

## Sources
- https://www.psdevwiki.com/ps2/Sony_WEGA_HVX_Series
- Dumps of KDL-L32HVX: https://archive.org/details/sony_2004_tv_dumps