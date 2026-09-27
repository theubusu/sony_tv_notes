# NAND
This describes the NAND setup of the models with 2 seperate 64MB TSOP48 chips.

The 2 NANDs are interleaved byte-by-byte, and also have a FTL system, where the logical block is encoded in the OOB area of both NAND's. Check `tool/emma_ftl.py` script for the exact logic.

The bootloader and other weird blocks at the start are ignored by the FTL, to linux device `/dev/nanda`, only the data portion is provided.

The resulting data is a DOS partition table containing one UVFAT16 partition.
```
Disk nx805.bin: 121 MiB, 126877696 bytes, 247808 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x00000000

Device     Boot Start    End Sectors  Size Id Type
nx805.bin1 *       31 247807  247777  121M  6 FAT16
```

## UVFAT16
UVFAT16 from what i can tell is a modification of FAT to bring linux style permissions to it. Standard extractors can choke up on these images, you can use `tool/uvfat2.py` script to extract.

The partition is also mounted on `/NAND`

The FAT partition contains the following in the root:
| name          | purpose |
|---------------|---------|
|.environment|Possibly stores env variables|
|.factory2.adj|Unknown|
|MS|Mountpoint for memory stick|
|SQBIN.IMG|Squashfs image of `/bin`|
|SQFIXED.IMG|Squashfs image of `/fixed`|
|SQLIB.IMG|Squashfs image of `/lib`|
|SQSBIN.IMG|Squashfs image of `/sbin`|
|SQSONY.IMG|Squashfs image of `/sony`|
|SQUSR.IMG|Squashfs image of `/usr`|
|VAR|Writable data directory|
|VMLINUX.FRZ|Linux kernel image|

Note that the squashfs partitions or kernel don't seem to be signed in any obvious way