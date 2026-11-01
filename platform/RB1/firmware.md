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