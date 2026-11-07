# NAND

As mentioned, the NAND is encrypted using hardware CBC cipher, it has a system and filesystem area, the system area is used by ROM/ABK to load the boot images and environment, and filesystem area has the sections accesible to linux.

> Note: Block is 262144 bytes, or 64 NAND pages(64*4096)

## System

The System Blocks area takes up until `FileSystemStartBlock`(in my case, and public dumps i checked it is 44), which hold system component images (DDRInit, ABK, Standby..) and Environment. The mapping is stored in `SystemTable`, and is decoded from the OOB of each system page (see `tool/sys_oob.py`). For each component, a redundancy copy is also stored.

#### Component types
| id          | type |
|---------------|---------|
|0x00|DDRInit + Standby|
|0x02|ABK|
|0x46|LogoFW|
|0x48|MiniKernel|
|0x50|?|
|0x60|Environment|

Note that block 0 is a reserved system parameters block, you cannot allocate or write it, it holds register table and fixed environment.

The system components (EXCEPT fixed environment/environment) seem to be encrypted with a different key/method than the rest of NAND data, so currently not known how to decrypt them from linux.

## Filesystem

The filesystem area starts at `FileSystemStartBlock` and is split into two sections - `nanda` and `nandb`. It also utilizes some sort of FTL, not fully known yet.

Dmesg driver log:
```
Bst2 Flash Memory driver
Raw NAND (x8) mode
1024MB (2048x2 blks, 64 pages, 4096+224 bytes/page), 8 bits ecc
nanda : 1 init.bad blocks, 0 acq.bad blocks, 179 free blocks
 nanda1
nandb : 0 init.bad blocks, 0 acq.bad blocks, 207 free blocks
 nandb1
```

### nanda
`nanda` is 844890112 bytes (805.75 MB) in size, and it contains one VFAT partition (`nanda1`). It is also used as the root device `root=/dev/nanda1 rootfstype=vfat`.

It is mounted at `/NAND` as `/dev/root`:   
`/dev/root /NAND vfat rw,noatime,nodiratime,fmask=0022,dmask=0022,codepage=cp437,iocharset=iso8859-1,quiet,batch_sync,posix_attr,comp_uni,errors=remount-ro 0 0`

It contains the system images in the root:
| name          | purpose |
|---------------|---------|
|MS|Mountpoint for memory stick|
|VAR|Writable data directory|
|sqandroid.img|Squashfs image of `/android`, Android's root.|
|sqbin.img|Squashfs image of `/bin`|
|sqdevel.img|Squashfs image of `/devel`|
|sqfixed.img|Squashfs image of `/fixed` (not updated)|
|sqsbin.img|Squashfs image of `/sbin`|
|sqsony.img|Squashfs image of `/sony`|
|squsr.img|Squashfs image of `/usr`|
|ssboot.fra|Snapshot boot image|
|vmlinux.fra|Linux kernel+coprocessors firmware image|

#### Note about squashfs
The squashfs images used have a custom compression definition where raw DEFLATE is used by linux crypto. Sony did that because the DEFLATE is hardware accalerated on this platform. The modification can be seen in kernel sources `fs/squashfs/crypto_wrapper.c`. So in order to extract the images, you need to modify your squashfs program to include this compressor.

Also noting that the squashfs images don't seem to be signed/verified in any way. But I haven't tried to replace them yet.

### nandb
`nandb` is 115343360 bytes (110 MB) in size, and it contains one EXT4 partition. It is used as the `/data` partition for Android   
`/dev/nandb1 /data ext4 rw,nosuid,nodev,noatime,barrier=1,data=ordered 0 0`
