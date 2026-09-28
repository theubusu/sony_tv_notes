# AZ2 platform (2011)

## SoC
CXD4727GB "X-Reality"
- Kernel mach: `ayubrd`
- Service manual name: `X-Reality`   

MIPS cpu. specifics unknown

## Kernel
`mips, 2.6.23.17-alp_nl_` (per Opera)

## NAND
- 256MB BGA63 OneNAND

There is not a single public NAND dump of any TV on this platform that i could find (probably because OneNAND programmers+BGA63 is expensive). Therefore, its not known whether the NAND is encrypted.

## GUI
NUX, introduced with this platform

## Opera
Version: 2.9  
Build: LSDK3400
  
### Access paths
|     | Path |
| --------  | -------- |
|Preferences|/dev/shm/opera_home/opera,ini|
|Saved session|/dev/shm/opera_home/sessions/autopera.win|
|Opera directory|/dev/shm/opera_home|
|Cache|/dev/shm/opera_home/cache|
|Plug-in path|/sony/usr/sony/share/webbrowser/plugins|
|User JavaScript folder|/dev/shm/opera_dir/userjs|

## OSS
Listing (latest saved): https://web.archive.org/web/20191019180628/http://oss.sony.net/Products/Linux/TV/KDL-32CX520.html 
Kernel: [Sony link](https://prodgpl.blob.core.windows.net/download/TV/common/zBiusZMzHFG8SB4KDXDP3A/linux-kernel.tgz) [Backup](https://s1.theubusu.xyz/0/uploads/sony%20kernels/2011_AZ2.tgz)


## Sources
KDL-26EX320