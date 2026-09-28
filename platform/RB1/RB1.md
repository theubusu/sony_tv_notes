# RB1 platform (2013)

## SoC
CXD4741GB(Ayu2)/CXD4748GB(Ayu2L) "X-Reality Pro"
- ARMv7L
- Kernel mach: `bst2brd`
- Service manual name: `Ayu2/Ayu2L`   
- Possibly custom by Sony Semiconductor Solutions [ref](https://www.arm.linux.org.uk/developer/machines/list.php?mid=3625)

SYMPTOM
Two versions of main board and tuner board have been used during production.
- BKE/BKT boards (AYU2).
- BLE/BLT boards (AYU2L)

NOTE:
- BKE/BKT (AYU2 processor): With Heat sink.
- BLE/BLT (AYU2L processor): Without Heat sink.

RAM: 1GB DDR3

### Ayu2L
- CPU (CA9(Arm Cortex A9?) Dual 800MHz)
- GPU (SGX543)
- Multi-format Dec.

```
Processor	: ARMv7 Processor rev 0 (v7l)
processor	: 0
BogoMIPS	: 1612.80

processor	: 1
BogoMIPS	: 1612.80

Features	: swp half thumb fastmult vfp edsp neon vfpv3 
CPU implementer	: 0x41
CPU architecture: 7
CPU variant	: 0x3
CPU part	: 0xc09
CPU revision	: 0

Hardware	: Bst2brd
Revision	: 0000
Serial		: 0000000000000000
```

## Kernel
`Linux version 2.6.35.14_nl-az4 (root@slave28.jp.sony.com) (gcc version 4.5.1 (20120207 (Sony CE Linux 8.1.0.3)) ) #1 SMP PREEMPT Mon Aug 8 13:28:53 JST 2016` (on `PKG4.600EUA`)
- `-az4` suffix is interesting, this is successor to AZ3 so makes some sense , but should be `rb1`

It seems to come with some custom `snsc_security` system, mostly for protecting the chroot for Android.

## NAND
- 1GB TSOP48 NAND (TC58NVG3S0FTAI0)

The NAND is fully encrypted, most likely using a CPU specific key. Therefore even though there are many NAND dumps, they are all useless

For more NAND layout info see `NAND.md`

## UART
The UART connector pinout can be found in service manuals of this or similar platforms, but it is seemingly disabled in production environment, completely quiet. There is also a JTAG connector, but it was not tested.

## Android
The platform has an Android subsystem. Read `android.md`

## GUI
"Genome", introduced with this platform. UI is rendered at 1080p , except on HD-ready TV.

## OSS
Listing: https://oss.sony.net/Products/Linux/TV/KDL-55W905A.html   
Kernel: [Sony link](https://prodgpl.blob.core.windows.net/download/TV/common/Lesm5juuv50ygMzqXgF7mg/kernel26.tgz) [Backup](https://s1.theubusu.xyz/0/uploads/sony%20kernels/2013_RB1.tgz)

## Useful/Misc notes
`info.txt` - output of some commands run from android (build.prop, id, mounts, root, dev, ps, dmesg, cpuinfo)

dmesg mentions `<6>[    1.878277] ABK: abk installed` , so it may also use the "ABK Monitor" bootloader

In dmesg:
```
<4>[    1.892078] squashfs: compression name is deflate
<4>[    1.892150] squashfs: crypto module deflate-w12 is used
```
this does not mean that the squashfs is encrypted, they are just using the deflate library of linux `crypto`. This modification is in kernel sources

The opera browser and nginx run as UID 500.
```
  873 500       0:00 nginx
  874 500       0:00 nginx
  1489 500       0:20 dtWebBrowserApp WEBBR
```

## Sources
KDL-24W605A