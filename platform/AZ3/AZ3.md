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


## Sources
KDL-55HX850