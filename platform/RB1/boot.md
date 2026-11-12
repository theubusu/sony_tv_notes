# Boot process

With the JTAG connection, we can analyze the early booting process of the CPU. The CPU starts with the STANDBY core, which is MIPS. So the BootROM code is MIPS 32bit Big endian. It only starts the ARM core later.

## BootROM
The (mask)BootROMs of Ayu2(CXD4745GB) and Ayu2L(CXD4748GB) have been dumped (avaliable in `bootrom`). They are basically the same with some minor changes

It its located at `0xbfc10000`, `0x10000` size.

### Booting
The bootrom can boot off:
- OneNAND
- RawNAND
- SPI (2 configs, either encrypted or not)
- MemoryStick
- Network(TFTP?)

The boot option is decided by straps/OTP.

### Loading
The loaded images are described by a 0x200 header stored on the selected boot source. ABK can also load and handle these images

Both the header and the data is stored ENCRYPYTED, and is then decrypted using a hardware device DMA. The bootrom does not have any crypto code or key material itself.

#### Image Header structure (all big endian)
| type          | purpose |
| --------      | -------- |
| u32           | magic1; must be 0xFAF0D5BE   |
| u32           | magic2; must be 0x30DA43F2   |
| u32           | magic3; must be 0x813442F2   |
| u32           | type magic; 0x0544BE__, last char determines type, see below  |
| [u8;16]       | MAC digest; also checked by hw operation after decrypt   |
| u32           | stored size of the payload   |
| u32           | decompressed size of  thepayload   |
| u32           | load address |
| u32           | entry point address |
| u32           | some paramater passed to the hw engine |
| u32           | address of ? |
| u32           | some paramater passed to the hw engine |
| u32           | unknown; possibly version? |

After header, follows 16 bytes of a version string.
The rest is padded with 0xFF

The data can be compressed using DEFLATE (hardware). One of the engine parameters possibly describes the compression, but cant be certain which since i havent seen an uncompressed image, and both values are always 1.

Image type table (for type magic):
| char          | name |
| --------      | -------- |
| 0x8C           | DDRInit   |
| 0xAC           | Standby   |
| 0x8D           | ABK   |
| 0xAF           | LogoFW  |
| 0xB0          | MiniKernel   |


- For NAND boot, it searches it for a valid header.
- For production SPI boot, it checks offset 0x200 (matches with RB2T eMMC boot SPI)
- For TFTP, it looks for file `ayu2_ddr?.code` and `ayu2_abk?.code` (Ayu2), `ay2l_ddr?.code` and `ay2l_abk?.code` (Ayu2L). The `?` is `a`-`p` decided by some strap value
- For MS boot, it looks for a valid boot MBR partition

## DDRInit
The bootrom loads and executes a small DDRInit program (it is MIPS code).  

Its exact behaviour was not analyzed, but its responsible for setting up the DDR RAM.

## Standby
Standby firmware is contained in the same image as DDRInit, and is also loader by bootrom

## ABK
After init DDR, the bootrom loads ABK, which is the main bootloader for the ARM core. After loading it to DDR, bootrom will bring up the ARM core pointed to the decrypted ABK code.

Latest versions seem to be:
- For Ayu2: `M5.001C`
- For Ayu2L: `M5.903C`

ABK then mounts the NAND's main FAT partition, and executes the linux kernel. You can interrupt its boot process and get to a password prompt by pressing `ESC` on TV booting. (described in UART section of main doc)

> todo more abk info

### Environment

ABK environment is loaded from NAND system area and decrypted. For format see `tool/env.py` 

The "fixed" environment, which holds has values that cannot be changed is located in the reserved system parameter NAND block 0, at offset 0x1000.
In my case it contained variables:
- `serial` - Main board serial number
- `macaddr` - Main board mac address
- `hdcp2xkey`
- `cipluskey`
- `tvid_service_tag`
- `nfxesn`
- `nfxkey`
- `tvid` - 16 byte seemingly random value
- `extract_path_fixed` - `/tmp/mnt/MSSONY/ABK/bin/exec_install.list`

The variable environment is placed in one of NAND system blocks with type `0x60`, In my case it contained variables:

The [placeholder] store an offset to the actual value inside fixed env, the value is not stored here.

- `EMK` - key involved in decryption of FRA, NOT device unique
- `BDI` - selected BDI
- `exttusize` - related to EXT partition (nandb1)
- `extfreeblk1k` - related to EXT partition (nandb1)
- `extrefintvl` - related to EXT partition (nandb1)
- `fatblock`
- `autoboot` - `on`
- `productid`
- `modelid`
- `serial` [placeholder]
- `macaddr` [placeholder]
- `hdcp2xkey` [placeholder]
- `cipluskey` [placeholder]
- `tvid_service_tag` [placeholder]
- `nfxesn` [placeholder]
- `nfxkey` [placeholder]
- `tvid` [placeholder]
- `extract_path_fixed` [placeholder]
- `ABBT` - Bad Block Table ?
- `boot` - `/vmlinux.fra`
- `subsystem_conf`
- `copied_service_tag`
- `preboot` - `/ssboot.fra`
- `logincount`
- `subsystem_mode`
- `nvm_factory_adj`

## LogoFW
LogoFW is loaded by ABK. It displays the SONY boot logo. It is MIPS code.

## MiniKernel
MiniKernel is loaded by ABK in case it needs to extract any FRA files (`extract_path` is set). It contains a whole linux kernel just for that purpose. (lol)