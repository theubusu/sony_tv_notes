# Firmware
The USB update firmware is shipped as a `.p09` file. The only copy I was able to find is the latest version `aa0211pn` - `sony_dtv_pkgaa0211pn.p09`

The `p09` container seems to be a basic package holding entries inside. For the structure and see in `tool/sony_pkg.py`

For my file it consists of 4 sections
- 1. (29,1 MB) label `DM09` - main software, it has some metadata including date and version `DB1.007W(REL)  1.25.8  Tue Mar 31 12:58:56 2009`(BOOT) `DM1.568A 1568          Thu Jan 31 11:50:11 2013`(PROGRAM) and some hashes(?) at the start, and then continues with encrypted data.
- 2. (1,12 MB) label `DV1.006A`, per service manual this is the "VIDEO PACK DATA" It seems to contain some raw bitmap data, the purpose is unknown.
- 3. (48,7 KB) label `DA1.008A` per service manual this is the "AUDIO PACK DATA". Purpose is unknown
- 4. (272 KB) no label, it contains multiple FRZ files with firmware for the SUB MICRO, including SM(Program) and SD(DATA) for different panels/models?