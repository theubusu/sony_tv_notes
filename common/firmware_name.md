# Firmware file naming

Based on `dtServiceLow` from AZ1

## Folder
`sony_dtvXXXXXXXXXXXX_MMMMMMMM`  

`X` is update_id `%012llX` (12-digit uppercase hexadecimal)   
`M` is model_id `%08X` (8-digit uppercase hexadecimal)
 
Example for AZ1 (AZ1H_v0531_EUH):   
`sony_dtv0FA00A00A0A0_00010100`   

update_id = 0x0FA00A00A0A0 (`UPDATE_ID` in release.version)     
model_id = 0x00010100 (`DOWNLOAD_ENCRYPTION_MODELID`/`DVB_UPDATE_ID` in release.version)   

## Firmware file
`MMMMMMMM_AAAABBBB.bin`

`M` is model_id `%08X` (8-digit uppercase hexadecimal)   
`A` is major version `%04X` (4-digit uppercase hexadecimal)   
`B` is minor version `%04X` (4-digit uppercase hexadecimal)

Example for AZ1 (AZ1H_v0531_EUH):   
`00010100_02130000.bin`   

model_id = 0x00010100    
major = 0x0213 (0531)   
minor = 0x0000    

Note: the name of bin file does not matter at least in AZ1, it will choose the first .bin file in the folder

## update ID's
- `0FA00A00A0A0` AZ1    2010
- `0FA10A01A0A1` AZ2    2011
- `0FA20A02A0A2` AZ3    2012
- `0FA20A03A0A3` AZ3SR  2012
- > Unknown 04
- `0FA30A05A0A5` RB1    2013
- `0FA40A06A0A6` RB2    2014
- > Unknown 07
- `0FA40A08A0A8` FMP-X7 2014
- `0FA50A09A0A9` GN1    2015
- `0FA60A0AA0AA` GN3    2016
- `0FA70A0BA0AB` GN5    2017
- `0FA80A0CA0AC` GN6    2018

### Structure
It seems to be:
- `0F` - always 0F
- `Ax` - second nibble is the year, A0=2010, A8=2018
- `0A` - always 0A
- `xx` - Incremental ID
- `A0` - always A0
- `Ax` - second nibble is the same as incremental ID

Mediatek linux TV and some AZ1 tv seems to use a different structure