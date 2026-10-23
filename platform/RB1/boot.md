# Boot process

With the JTAG connection, we can analyze the early booting process of the CPU. The CPU starts with the STANDBY core, which is MIPS. So the BootROM code is MIPS 32bit Big endian. It only starts the ARM core later.

## BootROM
The (mask)BootROMs of Ayu2(CXD4745GB) and Ayu2L(CXD4748GB) have been dumped (avaliable in `bootrom`). They are basically the same with some minor changes

It its located at `0xbfc10000`, `0x10000` size.

### Booting
The bootrom can boot off:
- NAND (2 configs)
- SPI (2 configs, either encrypted or not)
- MemoryStick?
- TFTP

The boot option is decided by straps/OTP.

### Loading
The two programs loaded by the BootROM (DDR, ABK) are described by a 0x40 header stored on the selected boot source.

Both the header and the data is stored ENCRYPYTED, and is then decrypted using a hardware device DMA. The bootrom does not have any crypto code or key material itself.

#### Header structure (all big endian)
| type          | purpose |
| --------      | -------- |
| u32           | magic1; must be 0xFAF0D5BE   |
| u32           | magic2; must be 0x30DA43F2   |
| u32           | magic3; must be 0x813442F2   |
| u32           | type magic; 0x0544BE8_, last char must be C for DDR, D for ABK  |
| [u8;16]       | digest; also checked by hw operation after decrypt   |
| u32           | size of the payload   |
| u32           | size of ? (maybe after processing)   |
| u32           | adress of the payload |
| u32           | probably entry point address |
| u32           | some paramater passed to the hw engine |
| u32           | address of ? |
| u32           | some paramater passed to the hw engine |
| u32           | unknown |

- For NAND boot, it searches it for a valid header.
- For production SPI boot, it checks offset 0x200 (matches with RB2T eMMC boot SPI)
- For TFTP, it looks for file `ayu2_ddr?.code` and `ayu2_abk?.code` (Ayu2), `ay2l_ddr?.code` and `ay2l_abk?.code` (Ayu2L). The `?` is `a`-`p` decided by some strap value
- For MS boot, it looks for a valid boot MBR partition

### Dump SRAM
From SRAM dump of bootrom (`0xbfc20000`), we can find some leftover data from previous boot including DDR program, ABK program header, NAND register table/script.

## DDR
The bootrom first loads and executes a small "ddr"(DDR init?) program (it is MIPS code).  

That program is loaded into SRAM. It can be and was also dumped.
- For Ayu2 dump version: `A2E1YM1.007	13/04/03_13:38`
- For Ayu2L dump version: `A2L1YM1.011	13/10/03_19:36`   

YMX.XXX version string matches what is in the service menu. So it represents that.

What this program does exactly was not analyzed yet.

## ABK
After init DDR, the bootrom loads ABK, which is the main bootloader for the ARM core. After loading it, bootrom will bring up the ARM core pointed to the decrypted ABK code. It is loaded in DDR, outside of SRAM, so it cannot be dumped with the current limitations.

We can see the version strings located after its program header in SRAM dump:
- For Ayu2 dump version: `M5.001C`
- For Ayu2L dump version: `M5.903C`

Again the MX.XXXC version matches what is in service menu, so that is ABK ver like i suspected.

ABK then mounts the NAND's main FAT partition, and executes the linux kernel. You can interrupt its boot process and get to a password prompt by pressing `ESC` on TV booting. (described in UART section of main doc)