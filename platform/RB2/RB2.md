# RB2 platform (2014)
Most information from RB1 should apply, the SoC used is the same.

## NAND/eMMC
- 1GB TSOP48 NAND
- 2GB(?) eMMC

eMMC seems to be used on some higher-end models. In both cases, they are fully encrypted.

## Android
This platform also has Android sub-system. It’s probably the same as in RB1, but wasn’t checked since i don’t have an RB2 TV.

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
