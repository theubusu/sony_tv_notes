# Firmware file

The firmware file is found as described in `common/firmware_name.md`  
It is processed by `dtServiceLow` 

## Structure
Starts with a 64 byte (encrypted) header, which is decrypted first
| type          | purpose |
| --------      | -------- |
| [u8;20]       | SHA-1 hash of the decrypted data   |
| [u8;12]       | unused   |
| u32           | magic; must be  0xDF81352E  |
| u32           | model |
| u32           | major |
| u32           | minor |
| u32           | total file size "datasize" |
| u32           | decrypted size |
| [u8;8]        | unused   |

Then `datasize`-0x40 bytes are read, decrypted, and the output is expected to be `decrypted size` bytes.   

The decrypted data is saved to  `/var/download/{model%08X}_{major%04X}{minor%04X}.frz`

The linux side checks that the first segment of the FRZ file has the type 0xF1, and uses a 32bit value at offset +0x05 as the total size of the update.

The bootloader's `preboot` value is then set to the path to the decrypted FRZ file. The bootloader will execute it on the next boot.

## Decryption key
The decryption key is calculated based on two bootloader environment variables: `frzkey` and `serial`

`serial` is first converted to a 32bit rolling value like:
```c
roll = 0;
for each byte c in serial:
    roll = ROL32(roll, 7) ^ c;
```

`frzkey` is then processed in 4 chunks of 8 characers (which implies that `frzkey` is a 32 character hex string)   
for each chunk, it converts it to an int, and XORs it with the `roll` value and the constant `0x853e0275`.   
The 4 final transformed values form `derived`

Then, it calls this function two times to produce the final AES key and IV:
```c
void ___key_descramble(uint *param_1,uint *param_2,uint param_3,uint param_4,uint param_5,
                      uint param_6,uint param_7,uint param_8,uint param_9,uint param_10)

{
  *param_1 = (param_3 >> 0x1e | param_3 << 2) ^ param_2[3];
  param_1[1] = (param_4 >> 0x1e | param_4 << 2) ^ *param_2;
  param_1[2] = (param_5 >> 0x1e | param_5 << 2) ^ param_2[1];
  param_1[3] = (param_6 >> 0x1e | param_6 << 2) ^ param_2[2];
  param_1[4] = (param_7 >> 0x1e | param_7 << 2) ^ *param_2;
  param_1[5] = (param_8 >> 0x1e | param_8 << 2) ^ param_2[2];
  param_1[6] = (param_9 >> 0x1e | param_9 << 2) ^ param_2[3];
  param_1[7] = (param_10 >> 0x1e | param_10 << 2) ^ param_2[1];
  return;
}
```

with the following arguments for the key:
```c
___key_descramble(_key,derived,0xde558682,0x82d3d767,0xab34fe1c,0x3a04918f,0xd7426139,0x4dcb2fe8,0x5bae88f1,0x853e0275);
```
and the IV:
```c
___key_descramble(_iv,derived,0xcf50262f,0x6c85d4db,0x567b2808,0xe1abf139,0x19f13ef4,0xb7a091ce,0xbc40d964,0x2ad67872);
```

### So where's the key?
Getting the key relies on having access to the bootloader variables of the device. Which means either rooting it and getting it from Linux, or from bootloader shell.   
We can get `serial` from NAND, but having just that does not help.    
The required key material for `frzkey` wasn't able to be retrieved by static analysis of the bootloader. (see `bootloader.md`)
