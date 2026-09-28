## NAND

Altough we can't access it directly from Android, we can infer some info about the NAND from the kernel logs and devices

```
Bst2 Flash Memory driver
Raw NAND (x8) mode
1024MB (2048x2 blks, 64 pages, 4096+224 bytes/page), 8 bits ecc
nanda : 1 init.bad blocks, 0 acq.bad blocks, 179 free blocks
 nanda1
nandb : 0 init.bad blocks, 0 acq.bad blocks, 207 free blocks
 nandb1
```

The NAND is split into two partitions - `nanda1` and `nandb1`.

### nanda
`nanda` is 844890112 bytes (805.75 MB) in size, and is a VFAT partition. It is also used as the root device `root=/dev/nanda1 rootfstype=vfat`.

It is mounted at `/NAND` as `/dev/root`:   
`/dev/root /NAND vfat rw,noatime,nodiratime,fmask=0022,dmask=0022,codepage=cp437,iocharset=iso8859-1,quiet,batch_sync,posix_attr,comp_uni,errors=remount-ro 0 0`

It very likely contains the squashfs images in its root. We can get their sizes and mountpoints:
| loop dev | mountpoint | size      |
| -------- | ---------- |---------- |
|loop0	   |/android	|68.2 MiB   |
|loop1	   |/bin		|4 KiB      |
|loop2	   |/devel		|9.16 MiB   |
|loop3	   |/fixed		|40.27 MiB  |
|loop4	   |/sbin		|4 KiB      |
|loop5	   |/sony		|87.6 MiB   |
|loop6	   |/usr		|28 KiB     |

### nandb
`nandb` is 115343360 bytes (110 MB) in size, and it is an EXT4 partition. It is used as the `/data` partition for Android   
`/dev/nandb1 /data ext4 rw,nosuid,nodev,noatime,barrier=1,data=ordered 0 0`

## Other loop mounts
```
/dev/loop7 /tmp/mnt/ccf/iptv.nvm vfat rw,relatime,fmask=0022,dmask=0022,codepage=cp437,iocharset=iso8859-1,quiet,posix_attr,comp_uni,errors=remount-ro 0 0
/dev/loop8 /tmp/mnt/ccf/skype.nvm vfat rw,nodev,noexec,noatime,nodiratime,fmask=0022,dmask=0022,codepage=cp437,iocharset=iso8859-1,shortname=winnt,quiet,posix_attr,comp_uni,errors=remount-ro 0 0
/dev/loop9 /tmp/mnt/ccf/mv_fs.nvm vfat rw,nodev,noexec,noatime,nodiratime,fmask=0022,dmask=0022,codepage=cp437,iocharset=iso8859-1,quiet,posix_attr,comp_uni,errors=remount-ro 0 0
/dev/loop10 /tmp/mnt/ccf/mv_db.nvm vfat rw,nodev,noexec,noatime,nodiratime,fmask=0022,dmask=0022,codepage=cp437,iocharset=iso8859-1,quiet,posix_attr,comp_uni,errors=remount-ro 0 0
/dev/loop11 /tmp/mnt/ccf/mv_store.nvm vfat rw,nodev,noexec,noatime,nodiratime,fmask=0022,dmask=0022,codepage=cp437,iocharset=iso8859-1,quiet,posix_attr,comp_uni,errors=remount-ro 0 0
/dev/loop12 /tmp/mnt/ccf/relatedsearch_store.nvm vfat ro,nodev,noexec,noatime,nodiratime,fmask=0022,dmask=0022,codepage=cp437,iocharset=iso8859-1,shortname=winnt,quiet,posix_attr,comp_uni,errors=remount-ro 0 0
/dev/loop13 /tmp/mnt/ccf/richmeta_map.nvm vfat rw,nodev,noexec,noatime,nodiratime,fmask=0022,dmask=0022,codepage=cp437,iocharset=iso8859-1,quiet,posix_attr,comp_uni,errors=remount-ro 0 0
```

## NAND related processes
```
root      238   2     0      0     ffffffff 00000000 S nandwork
root      242   2     0      0     ffffffff 00000000 S nandwork-nandb
```