# eMMC
On RB2, eMMC is used in higher-end TV models.
The chip capactity is 4GB, but it is used in ENH mode(?), so data capacity is actually 2GB, with added redundancy.

The boot0 and boot1 area of eMMC are not used.

Like on NAND, the data is fully encrypted on the eMMC with a device-specific key, and the data is seperated into system and filesystem areas.

## System
The system block table is located at `0x8000` offset on the eMMC. This offset is retrieved from ABK by `abk_glue_emmc_get_sys_table_pos`. It is indentified by magic `0xb4b98a94`

See `tool/emmc_sys.py` for the structure.