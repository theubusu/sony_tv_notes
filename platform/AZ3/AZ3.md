# AZ3 platform (2012)

## SoC
CXD4733GB "X-Reality"
- Kernel mach: `ayubrd`
- Same mach as AZ2
- Service manual name: `Atreyu`   

Interesting note: "Toshiba Atreyu" mentioned [here](https://github.com/kousik1004/ResumeXtract/blob/39bfeea10fede11ec4ff22a7bf6fbbc96b6eeb0d/sample_resumes/batch_9/5775_Asit_Shrivastava.txt#L184) - possibly Toshiba SoC?

MIPS cpu. specifics unknown

## Kernel
`mips, 2.6.23.17-alp_nl_` (per Opera)   
- Same kernel as AZ2

## NAND
- 256MB BGA63 OneNAND

There is not a single public NAND dump of any TV on this platform that i could find (probably because OneNAND programmers+BGA63 is expensive). Therefore, its not known whether the NAND is encrypted.

## GUI
NUX, slighly modified main menu design compared to 2011 (icons at the bottom now have labels)

## Opera
Version: 3.2   
Build: LSDK4510
  
### Access paths
|     | Path |
| --------  | -------- |
|Preferences|/dev/shm/opera_home/opera.ini|
|User profile|/dev/shm/opera_home|
|Cache|/dev/shm/opera_home/cache|
|Plug-in path|/sony/usr/sony/share/webbrowser/plugins|
|User JavaScript folder|/sony/usr/sony/bin/$OPERA_DIR/userjs|
|User styles folder|/dev/shm/opera_dir/mystyles|

## SEN/BIVL
Indexes(EU): https://applicast.ga.sony.net/WsIndexes/AZ3_EU.xml

Interesting note:
- https://github.com/CFSworks/nimue/issues/6
Apparent bypass of widget signatures and run from USB. I wasn't able to confirm this.

## OSS
Listing (latest saved): https://web.archive.org/web/20191019180723/http://oss.sony.net/Products/Linux/TV/KDL-55HX75G.html   
Kernel: [Sony link](https://prodgpl.blob.core.windows.net/download/TV/common/qNe4FQvq2i_B0gV8BTteCw/linux-kernel.tgz) [Backup](https://s1.theubusu.xyz/0/uploads/sony%20kernels/2012_AZ3.tgz)


## Sources
KDL-55HX850