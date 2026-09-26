# Firmware file naming

Based on `dtServiceLow` from AZ1

## Folder
`sony_dtvXXXXXXXXXXXX_MMMMMMMM`  

`X` is (purpose unknown) `%012llX` (12-digit uppercase hexadecimal)   
`M` is model `%08X` (8-digit uppercase hexadecimal)
 
Example for AZ1:   
`sony_dtv0602000A0213_00050301`   
X = 0x0602000A0213   
model = 0x00050301   

X probably has region info.

## Firmware file
`MMMMMMMM_AAAABBBB.bin`

`M` is model `%08X` (8-digit uppercase hexadecimal)   
`A` is major version `%04X` (4-digit uppercase hexadecimal)   
`B` is minor version `%04X` (4-digit uppercase hexadecimal)

Example for AZ1:   
`00050301_02050000.bin`   
model = 0x00050301    
major = 0x0205   
minor = 0x0000    

Note: the name of bin file does not matter at least in AZ1, it will choose the first .bin file in the folder

## Some model ID
AZ1 `0x00050301`   
AZ2 `0x00000100`   
AZ3 `0x00001201`   
RB1 `0x00002100`   
