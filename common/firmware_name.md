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
- AZ1  `0FA00A00A0A0`
- AZ2  `0FA10A01A0A1`
- AZ3  `0FA20A02A0A2`
- AZ3  `0FA20A03A0A3` (hiend model)
- RB1  `0FA30A05A0A5`
- RB2  `0FA40A06A0A6`
