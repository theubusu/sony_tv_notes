# WAX3 (JP, 2007)

This is a 2007 Japan platform/chassis used in KDL-J3000/J5000 series TV.

## SoC
- NEC EMMA2TH (D61162AF1) MIPS
- 2x64MB DDR2 SDRAM RAM = 128MB

## NAND/NOR
- NOR: 29LV200TC 256KB, contains the ABK Monitor/bootloader and environment
- NAND: 2xK9F5608U0D 32MB = 64MB

NAND has interleaved and FTL setup

In NOR, the bootloader area seems to be encrypted. Environment encryption is the same as in SF1EG, with serial being at 0x3FF00, fixed env at 0x3c000, and environment at 0x38000

### Files in NAND:
The root partition is a "UVFAT16"

| name          | purpose |
|---------------|---------|
|`cramfsimage.sony`| Squashfs image of `/sony`|
|`cramfsimage.fixed`| Squashfs image of `/fixed`|
|`/bin/vmlinux.frz`| Linux kernel image|

Note: YES, even though the files are named `cramfsimage`, they are actually SquashFS 2.1 files. They seem to be a bit weird which can cause extraction failures on standard tools.

## Kernel
`Linux version 2.4.17_mvl21-dth (root@kusatsu) (gcc version 2.95.3 20010315 (release/MontaVista)) #1 Fri Jul 20 10:02:15 JST 2007`

## UI/AppliCast
This is most likely the first platform to come with the inclusion of X2 and AppliCast. 

The UI is fully based on X2 with the usual `__system` structure. It is XMB and rendered at 960x540

It comes with a preloaded widget at `/sony/usr/sony/bin/__system/misc/WidgetSystem/InitialWidget`

## Firmware
This also has the earliest known implementation of the "dfwrap" firmware container, used all the way up to the end. 

The naming is also the same (model id comes from `DOWNLOAD_ENCRYPTION_MODELID` in `release.version`), except there is no update id in the folder path, so it's just `sony_dtv`.

It has the exact same frzkey+serial deviration as described in AZ1's `firmware.md` implemented in `dtServiceLow`, and in this case we can actually get frzkey from the fixed env:
- serial: `A-1217-097-A_7177442`
- frzkey: `021d39113ac0fef9fee2c0ffedf6850e`

However it isnt very useful since we don't have any firmware files for it.

## Sources
A BJ1 board(1-873-010-15) (which I've now found is from a KDL-26J3000), which somehow made its way onto a [Polish auction site](https://allegro.pl/oferta/main-1-873-010-15-nr-2433-16722469684). How it ended up here will be my life long mystery.