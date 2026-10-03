# RB2 platform (2014/2015)
SoC information from RB1 should apply, the same are used.

## NAND/eMMC
- 1GB TSOP48 NAND
- 4GB eMMC THGBMAG5A1JBAIR (in ENH mode(?), so data capacity is actually 2GB)

eMMC seems to be used on some higher-end models. In both cases, they are fully encrypted.

RB2T chassis seems to use 2 4GB eMMC's. One of them is mostly empty, its probably used for extra storage

### 2Mb SPI-ROM(SerialNorFlash) for eMMC boot
In case of eMMC device, it will boot from an external SPI flash. The flash contains a small 0x1200 encrypted blob, which possiblys sets up the eMMC, and continues the boot from there.

## Android
This platform also has Android sub-system. It’s probably the same as in RB1, but wasn’t checked since i don’t have an RB2 TV.

Additionally seems to have an Android media player app.

## GUI
Internally also called „Genome” like in RB1, but its a different full-screen style menu, with panel navigation.

## SEN/BIVL
Indexes(EU): https://applicast.ga.sony.net/WsIndexes/RB2_EU.xml

## OSS
Listing: https://oss.sony.net/Products/Linux/TV/KDL-32W705B.html   
Kernel: [Sony link](https://prodgpl.blob.core.windows.net/download/TV/common/xsuUY5l6aneXFxXYkOcoGQ/kernel26.tgz) [Backup](https://s1.theubusu.xyz/0/uploads/sony%20kernels/2014_RB2.tgz)

## PKG (RB2G/RB2T)
| pkg       | dest | id      |
| --------  | ---------- |---------- |
| EUA       | DVB-AEPT2S2_NO-NR, DVB-AEPT2S2_BASE       |sony_dtv0FA40A06A0A6_00003100|
| EUB       | DVB-AEPT2S2_MHP   						|sony_dtv0FA40A06A0A6_00013100|
| GAA       | DTMB-HK_BASE, DVB-TW_BASE, DVB-GAT2_BASE, DVB-GAT2_NO-IND, DVB-GAT2_NO-CI, DVB-LTN_BASE      |sony_dtv0FA40A06A0A6_00003201|
| GAB       | DTMB-CN_BASE        						|? |
| AAA       | ATSC-LTN_BASE, ATSC-UC_BASE      			|sony_dtv0FA40A06A0A6_00003301|
| BRA       | ISDB-LTN_BASE       						|? |
| BRB       | ISDB-LTN_NO-GIN     						|? |
| JPA       | ISDB-JP_BASE        						|?|

## FMP-X5/FMP-X10
These two 2014 4K media player models use the Ayu2 CPU and the RB2 software. FMP-X10 used the `AAQ` PKG, but firmware is nowhere to be found now.

## Notes/Useful
- Level 3 Confidential Service manual for RB2G - contains UART/JTAG pinouts, board schematic and connections of AYU2L(So also useful for RB1) - http://televid-sib.org/index.php?topic=22363.msg148626#msg148626