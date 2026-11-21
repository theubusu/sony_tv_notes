# eMMC
On RB2, eMMC is used in higher-end TV models.
The chip capactity is 4GB, but it is used in ENH mode(?), so data capacity is actually 2GB, with added redundancy.

The boot0 and boot1 area of eMMC are not used.

Like on NAND, the data is fully encrypted on the eMMC with a device-specific key, and the data is seperated into system and filesystem areas.

## System
The system block table is located at `0x8000` offset on the eMMC. This offset is retrieved from ABK by `abk_glue_emmc_get_sys_table_pos`. It is indentified by magic `0xb4b98a94`

See `tool/emmc_sys.py` for the structure.

## Filesystem

The filesystem area is one section `nanda`, which has two partitions, `nanda1` and `nanda2`   
(yes, nand naming is still used even if eMMC is used, probably for compatibility)

Dmesg driver log:
```
Bst2 Flash Memory driver (v131203)
eMMC (non MeNO) mode
eMMC: 1888MiB, Toshiba 004G90 (rev 0x51, date 0x71, serial 0xd2c64ded)
nanda1 nanda2
```

### nanda1
`nanda1` is 1572847104 bytes (~1500MB) in size, and it is a VFAT partition It is also used as the root device `root=/dev/nanda1 rootfstype=vfat`.

It is mounted at `/NAND` as `/dev/root`:   
`/dev/root on /NAND type vfat (rw,noatime,nodiratime,fmask=0022,dmask=0022,codepage=cp437,iocharset=iso8859-1,quiet,batch_sync,posix_attr,comp_uni,errors=remount-ro,discard)`

It contains the system images in the root, as described in RB1's `NAND.md`

### nanda2
`/dev/nandb1` points to `/dev/nanda2` here, also for compatibility reason.

`nanda2` is 209715200 bytes (200 MB) in size, and it is an EXT4 partition. It is used as the `/data` partition for Android   
`/dev/nandb1 on /android/data type ext4 (rw,nosuid,nodev,noatime,barrier=1,data=ordered,discard)`