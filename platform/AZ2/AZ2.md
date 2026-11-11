# AZ2 platform (2011)

## SoC
CXD4727GB "X-Reality"
- Kernel mach: `ayubrd`
- Service manual name: `X-Reality/Atreyu`   

MIPS cpu. specifics unknown

RAM: 512MB DDR3

## Kernel
`mips, 2.6.23.17-alp_nl_` (per Opera)

## NAND
- 256MB BGA63 OneNAND

There is not a single public NAND dump of any TV on this platform that i could find (probably because OneNAND programmers+BGA63 is expensive). Therefore, its not known whether the NAND is encrypted.

## Firmware
The format is the same as described in AZ1's `firmware.md` (see `tool/pkg_dec.py` for auto decrypt)

### Key
It turns out, AZ2/AZ3 use the same key deviration method as RB1, only as big-endian rather than little-endian (see `tool/pkg_key.py`)

- key: `41f43ecdfab621f69f6e8100e9c4e9e1`
- iv: `05e2bc7943ee2f056a51d95387796b3a`

### Contents
The decrypted data is a single FRA file (see RB1's `fra.md`). We cannot decrypt this for now, since we don't have access to the system (and RB1's Ayu2 cannot decrypt it, has different keys and/or procedure).

### Exploitation
We can't be sure how exactly the update is handled (not TAR file like on RB1/RB2), so not sure if any exploitation is possible. However because we can easily modify the header, it could lead to possible downgrade firmware or install from different model.

## GUI
NUX, introduced with this platform

## Opera
Version: 2.9  
Build: LSDK3400   
Platform: Linux   
System: `mips, 2.6.23.17-alp_nl-`

### Browser identification
`Opera/9.80 (Linux mips; U; InettvBrowser/2.2 (00014A;SonyDTV115;0002;0100) KDL26EX320; CC/POL; pl) Presto/2.7.61 Version/11.00`
  
### Access paths
|     | Path |
| --------  | -------- |
|Preferences|/dev/shm/opera_home/opera.ini|
|Saved session|/dev/shm/opera_home/sessions/autopera.win|
|Opera directory|/dev/shm/opera_home|
|Cache|/dev/shm/opera_home/cache|
|Plug-in path|/sony/usr/sony/share/webbrowser/plugins|
|User JavaScript folder|/dev/shm/opera_dir/userjs|

## SEN/BIVL
Indexes(EU): https://applicast.ga.sony.net/WsIndexes/AZ2_EU.xml

## OSS
Listing (latest saved): https://web.archive.org/web/20191019180628/http://oss.sony.net/Products/Linux/TV/KDL-32CX520.html 
Kernel: [Sony link](https://prodgpl.blob.core.windows.net/download/TV/common/zBiusZMzHFG8SB4KDXDP3A/linux-kernel.tgz) [Backup](https://s1.theubusu.xyz/0/uploads/sony%20kernels/2011_AZ2.tgz)

## Notable/interesting hardware 
- KDL-55HX80R/46HX80R/40HX80R/32EX30R/26EX30R - Japan only - TV with built-in BluRay recorder(bdre8gtv) [verup](https://www.sony.jp/bravia/update/usbup20150122b.html)

## Sources
KDL-26EX320