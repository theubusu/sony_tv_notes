# Lyon
Lyon is the codename for the secondary CPU/decoder (`extdec`/`extcpu`) used alongside Ayu2 in 4K RB2 TV's and media player. It is labeled "XVAD1", model `CXD4754GB`.

It contains a main ARM core, standby MIPS core, and a seperate VPC core reffered as "ALLEGRO".

It includes the H.265 4K decoder that Ayu2 lacks, it handles media playback and some DRM functionality. HDMI output on media player/Panel on TV comes from Lyon.

Lyon has its own Linux kernel, ABK, and system partitions, stored on a seperate eMMC.

## Hardware
### RAM
In total , there is 1.5G of RAM , organized as:
- 2x 4Gbit `H5TQ4G63AFR` = 1G total
- 4x 1Gbit `H5TQ1G63EFR` = 512M total

It might be split between the different subcore of Lyon.

### eMMC
Lyon has same layout and model of eMMC as Ayu2, see `emmc.md`. It uses its own encryption, so Ayu2 can't decrypt its data.

Lyon might be able to boot directly from eMMC, unlike Ayu2 which uses a seperate SPI rom.

### Extra Interface
- RGMII
- PCIe
- USB 3.0
- MS

## Communication with Ayu2
### GPIO
Ayu2 gets two GPIO signals to control Lyon:
- `LY_UPDATE` Ayu2 GPIO 39(OUT), Lyon GPIO 15(IN)
- `LY_BOOT_NOTIFY` - Ayu2 GPIO 21(IN), Lyon GPIO 16(OUT)

Getting and setting the signals is exposed on `/dev/fradec` by ioctl.

In normal operation `LY_UPDATE` is 1, and `LY_BOOT_NOTIFY` is 0.   
In update mode, `LY_UPDATE` is 0, and `LY_BOOT_NOTIFY` is 1

To enter update mode from normal, set `LY_UPDATE` to 0, and reset lyon.

### USB
The main data communication path between the two CPUs is by USB.

In normal operation, the USB device is connected as a Ethernet gadget:
```
Bus 002 Device 003: ID 049f:505a Linux 2.6.35.14_nl-ln1 with sud_udc Ethernet Gadget
```
Here you can also see its  kernel version - `Linux 2.6.35.14_nl-ln1`, same base as Ayu2, with `ln1` suffix.

It is given ip address 192.0.2.213
```
usb0      Link encap:Ethernet  HWaddr 36:13:40:B2:C8:54
          inet addr:192.0.2.213  Bcast:192.0.2.215  Mask:255.255.255.252
          UP BROADCAST RUNNING MULTICAST  MTU:15800  Metric:1
          RX packets:1357 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1372 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:98645 (96.3 KiB)  TX bytes:115738 (113.0 KiB)
```

On boot, it downloads exception logs to `/var/emlog_lyon.txt` and `/var/vpcexception_lyon`(for VPC), gets is firmware versions, and sets the clock.

Media streaming is done over this connection

### USB  (Update mode)
In update mode, Lyon exposes a small vfat partition , on a "Sony TV File Gagdet":
```
Bus 002 Device 005: ID 0525:a4a5 SONY TV File Gadget
```

In MiniKernel extract process, it is mounted at `/tmp/mnt2`, and Lyon's FRA files are transferred there to be installed.
```
/dev/sdb on /tmp/mnt2 type vfat (rw,relatime,fmask=0000,dmask=0000,allow_utime=0022,codepage=cp437,iocharset=iso8859-1,quiet,posix_attr,comp_uni,errors=remount-ro)
/sony/usr/sony/bin # ls -la /tmp/mnt2
drwxrwxrwx    2 root     root        16384 Jan  1  1970 .
drwxrwxrwx   15 root     root          680 Nov 22 12:36 ..
```

The parition is 100MB in size, and has a label `dummy`, it is probably a temporary partition in RAM, rather than an actual exposal of Lyon's eMMC.

### V-by-One
There is a V-by-One connection from Ayu2 to Lyon, which is most likely used for Ayu2's graphics/video.

## Version
(FMP-X5 PKG2.059EUP)

From exception log:
```
SOFTWARE_VERSION = DM0.0J00AA
PACKAGE_TIME = 2015/04/30:21:31:17
PACKAGE_HOST = panther-jenkins6
PACKAGER = root
CELINUX_VERSION = 8.0
KERNEL_BASE_VERSION = 8_1_DTV14_20130710
PEM_VERSION = 
P4_SYNC_LABEL = @436883
CONFIGFILE    = 
P4_TOP_PATH   = //14BOX/Panther/Exp/Release/TypeB-Release-GM10
P4DEPOT_NAME  = 14BOX
P4BASE_NAME  = TypeB-Release-GM10
P4_SYNC_OPTIONS = -p
CONFIGFILE_PATCHED=defconfig-ayu2-one-binary-one-to-ext-dec-ayu2-to-lyon-one-to-panther-b-develop-to-product-disable-assert.patched
```

From boot response:
```
HOST_CPU_MAIN_PROG_VERSION: LM2.059LNQ
VPC_FIRMWARE_VERSION: WF5.703W00AA
VENDOR_FIRMWARE_VERSION: SW_VER_40_70_06
STANDBY_CPU_PROG_VERSION: YM1.220W00AA
BOOT_PROG_VERSION: M6.308C
MP_RELEASE_HOT_MAIN_PROG_VERSION: LM2.027LNQ
NVM_DATA_VERSION: DD8.211W00AA
PACK_DATA_VERSION: PK0.072W00AA
```