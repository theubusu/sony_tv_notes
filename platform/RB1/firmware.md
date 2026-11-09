# Firmware (update)

The outer firmware file format is the same as described in AZ1's `firmware.md`, so a SHA-1 and a simple header appended to encrypted file. It is not signed. 

## Key
The firmware file AES-128-CBC key is derived based on hardcoded constants in `dtServiceLow` and seems to work for all regions of RB1 and also RB2 firmware.
- key: `cd3ef441f621b6fa00816e9fe1e9c4e9`
- iv: `79bce205052fee4353d9516a3a6b7987`

## Contents
The decrypted content of the firmware file is a TAR archive containing FRA-encrypted packages (see `fra.md`) and metadata list:
- `13_RB1_XXXXXXXX_VXXXX_VERX.XXXXXX_V.fra` - contains version information: `release.pkg.version` and md5sum of main files: `md5sum_PKG.txt`
- `13_RB1_ADX.XXXXX_DP_user.fra` - Android data package
- `13_RB1_AMX.XXXXX_A_user.fra`- Android package, contains `sqandroid.img` and `release.android.version`
- `13_RB1_CMX.XXXXXX_CP_relnand.fra` - CoreTV package, contains main squashfs partitions, `release.core.version` and `/var` EDID/eeprom data
- `13_RB1_SYSX.XXXXX_S.fra` - System components package, contains DDRInit, Standby, ABK, LogoFW, MiniKernel. Not handled by linux side updater.
- `exec_install.list` - List of all .fra packages

Every package also comes with an executable section that can extract it and install the system components (in SYS package) if they are present, in that case those components are also additionally decrypted (see `tool/dec_sys.py`). Those are then in the format of boot image described in `boot.md`

When extracting the FRA packages (using `/dev/fradec`), the linux-side updater ignroes the first executable section and combines the rest into one stream.

The decrypted packages have a format that can perform various actions (set env, create/delete files, update sys,bdi.panelid..) also depending on the device model , see `tool/do_pkg.py`. 

## Exploitation
As mentioned before, the update file is not signed, it only utilizes an encrypted SHA1 hash for integrity checking. 

Becuse of that, we can quite easily fabricate our own firmware file that will be accepted and processed by the TV (see `tool/fw_hax/mkfw.py`) 

The processing in question is extracting the inner TAR archive. It is done as follows:
```c
iVar2 = execlp("tar","tar","-xvf",*(undefined4 *)(param_1 + 0x18),"-C","/var/download",0);
```

This is pretty naive, because busybox's tar will happily extract archives with *ABSOLUTE PATHS*
(example crafted by `tool/fw_hax/tartest.py`)
```
/sony/usr/sony/bin # tar -xvf /tmp/test.tar -C /var/download
/NAND/hello.txt
/sony/usr/sony/bin # cat /NAND/hello.txt
hello from NAND
```

So we can literally write to anything thats writeable on the filesystem using the manufactured file. However we should be very careful with the changes; anything goes wrong and the TV could be bricked forever.

If squashfs replacement is confirmed, this can be used to directly replace one of the images at `/NAND`, although this might cause some unforseen troubles, because we will be rewriting an already mounted loop image with no additional verifications.

Another interesting thing to replace would be the writeable nginx config files at `/var/nginx` (`nginx.conf`, `sites-avaliable`, `sites-configured`)

This could also possibly allow to create symlinks on the NAND filesystem.

### Note about process
The TV will reboot attempting to install the update after extracting the TAR, but since our TAR has no actual update packages, it will not actually install anything and boot normally, so it will get caught in a loop detecting the update on the USB again and rebooting, so after it reboots for the first time, you need to unplug the USB to prevent that.

Also this does not mean we can create modified FRA packages, this only involves the inital TAR layer.