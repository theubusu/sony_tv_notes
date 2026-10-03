# AZ1 platform (2010)

## SoC
NEC/Renesas EMMA3T series   
- EMMA3TH For AZ1H
- EMMA3TL2 For AZ1L

Both are MIPS-based CPUs. Check `emma3tl2.pdf` datasheet for more info.

## Kernel
`2.6.23.17-alp_nl-`   
`Linux version 2.6.23.17-alp_nl- (root@slave113) (gcc version 4.1.2 20090526 (Sony CE Linux 5.0.3.0)) #1 Tue Nov 18 20:35:25 JST 2014` (nx805)

## NAND
Either:
- 2x64MB TSOP48 NAND chips (interleaved, more in `NAND.md`, possibly this was used only on the EMMA3TH models)
- 1x128MB OneNAND BGA63 chip

The NAND is not encrypted.

## UART
UART should be enabled on this platform as seen the logs published online, and will output the kernel log, unknown if any input is possible.

## Bootloader
See `bootloader.md`

## Firmware
See `firmware.md`

## GUI
XMB+NSX
- [Sony Monolithic TV Interface](http://www.jongaiser.net/pj_monolith.html)

## Useful
- dumps of file `release.version` from both NAND dumps and also from below logs in the folder with same name
- various UART logs from https://acassis.wordpress.com/2011/08/08/log_sony_bravia/ and https://acassis.wordpress.com/2014/10/08/more-sony-kdl-32ex405-logs/ in `logs.txt`

## SEN/BIVL
Indexes(EU): https://applicast.ga.sony.net/WsIndexes/AZ1_EU.xml

## OSS
Listing (latest saved): https://web.archive.org/web/20191019180653/http://oss.sony.net/Products/Linux/TV/KDL-40NX700.html   
Kernel: [Sony link](https://prodgpl.blob.core.windows.net/download/TV/common/qTYy33LvLhXL5sVA67wWMg/kernel26.tgz) [Backup](https://s1.theubusu.xyz/0/uploads/sony%20kernels/2010_AZ1.tgz)

## Sources
2 NAND dumps: KDL-40NX700 and KDL-40NX805. Both are on EMMA3TH CPU, and the 2x64MB NAND setup.