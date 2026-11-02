# RB2 platform (2014/2015)

# Most information from RB1 should also apply to RB2.

## SoC
SoC information from RB1 applies, the same are used.

## NAND/eMMC
- 1GB TSOP48 NAND
- 4GB eMMC THGBMAG5A1JBAIR (in ENH mode(?), so data capacity is actually 2GB)

eMMC seems to be used on some higher-end models. In both cases, they are fully encrypted.

RB2T chassis seems to use 2 4GB eMMC's. One of them is mostly empty, its probably used for extra storage

### 2Mb SPI-ROM(SerialNorFlash) for eMMC boot
In case of eMMC device, it will boot from an external SPI flash. The flash contains a small 0x1200 encrypted blob, which possiblys sets up the eMMC, and continues the boot from there.

## Android
This platform also has Android 4.0.4 based sub-system like RB1. See its notes for more info

However, Crucial difference: The browser app is missing. So installing APKs that way like in RB1 isnt possible.

## Firmware (Update)
See RB1's `firmware.md`, RB2 uses the same firmware keys and format, also RB1 tv's can decrypt RB2 fra packages (because keys are SoC specific, and both use same SoC series).

RB2 firmware packages also additionally ship with LYON package for the sub-cpu on some higher-end TVs:
```
LYON_PACKAGE_VERSION=LM3.006LNA
LYON_PACKAGE_NAME=14_RB2LN_LM3.006LNA_LP_relnand.fra
LYON_SYSTEM_PACKAGE_NAME=14_RB2LN_SYS3.006WW_S.fra
LYON_VERSION_PACKAGE_NAME=14_RB2LN_00003100_V1056_VER3.006LNA_V.fra
```

These cannot be decrypted by Ayu2, since Lyon is a seperate soc with different keys.

## GUI
Internally also called „Genome” like in RB1, but its a different full-screen style menu, with panel navigation.

plus DUX (Discovery UX)

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

## Notable/Interesting hardware
### FMP-X5/FMP-X7/FMP-X10
These 2014 4K media player models use the Ayu2 CPU and the RB2(based) software. 

FMP-X5(Europe/Canada) never had software update released. [sm](https://elektrotanya.com/sony_fmp-x5_fmp-x5-1_4k-hd-mp_ver.1.0_rm.pdf/download.html)

FMP-X7(Japan) software update site is up at https://www.sony.jp/bravia/update/usbup_fmp-x7.html, `sony_boxupdate_2014_2074_jpp_auth.zip`, `PKG2.074JPP` but the download link is down. It does say it's update ID however - `sony_dtv0FA40A08A0A8_00413500`

FMP-X10(US) - latest software update `PKG2.071AAQ` released on 04/05/2017, was avaiable [here](https://www.sony.com/electronics/support/home-video-4k-ultra-hd-media-players/fmp-x10/downloads/W0011110), not archived, firmware or even the ID is nowhere to be found now. [sm](https://elektrotanya.com/sony_fmp-x10_4k-hd-mp_ver.2.0_rm.pdf/download.html)

## Notes/Useful
- Level 3 Confidential Service manual for RB2G - contains UART/JTAG pinouts, board schematic and connections of AYU2L(So also useful for RB1) - http://televid-sib.org/index.php?topic=22363.msg148626#msg148626