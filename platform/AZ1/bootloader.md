# Bootloader
The bootloader used is Sony's "ABK Monitor". Both dumps i have contain version M3.009C from Mar 30 2010, 20:18:31.

It contains support for networking, Memory sticks, Fat filesystem, AES.

For some reason, in NAND, each 0x4000 chunk of the bootloader is repeated twice. This is also the case in many older Sony TVs (for redundancy/recovery?). So you need to remove every second 0x4000 region to get the proper bootloader. 

Also, every 0x4000 block starts with 4 bytes of some sort of index or address(?), table:
```
[00]   00000120    288
[01]   00010000    65536
[02]   00018000    98304
[03]   00020000    131072
[04]   00028000    163840
[05]   00030000    196608
[06]   00038000    229376
[07]   00040000    262144
[08]   00048000    294912
[09]   00050000    327680
[10]   00058000    360448
[11]   00060000    393216
[12]   00068000    425984
[13]   00038000    229376
```
It's purpose is unknown. In order to decompile the bootloader properly this must be removed.

At the end of the bootloader region there is also a 0x1d80 chunk of data that varies per device. It looks like some garbage mostly filled by 0xff bytes.

## Analysis
After removing the duplicated blocks and index values, the bootloader can be loaded at `0x8004fdb8` load address as MIPS-BE 32bit, and everything decompiles cleanly.

## Environment variables
The environment variables are loaded from the `.environment` file in the root of the filesystem, and possibly another 0x1f000 blob from somewhere else (currently unknown). They are both encrypted using AES, and then another simple XOR scheme based on the `serial` value (check `tool/dec_env.py`).

### Note: `serial`
The `serial` value is not stored in the store mentioned above. Instead, it  is read from offset 0x200 at the start of the NAND data area (immediately following the boot sector).   
Example for NX805: `A1749491A_9029076`.    
It is not obfuscated or encrypted in any way.  
This value is different per device. It also ends with a Checksum8 after the null byte in NAND.    
Note that this is not the device's serial number.

## AES keys
The AES keys used to decrypt the environment are loaded from an object at `8000218c + 0xc`. The bootloader itself seemingly never writes to that address, so it is probably populated by an earlier stage (Boot/mask ROM?)

## Command table (output of help command)
```
<<< ABK Monitor >>>

d[b|w|l] [<Addr>] [<size>]        : dump [byte|word|longword]-access
m[b|w|l] <Addr> [<data>]          : modify [byte|word|longword]-access
f[b|w|l] <start> <end> <data>     : fill [byte|word|longword]-access
cm <src> <dist> <size>            : copy memory
c <src> <dist> <size>             : compare memory
a [<Addr>]                        : assemble
l [<Addr>] [<size>]               : disassemble
lr [direct|normal]                : change disassemble register mode

boot [<flags>]                    : execute file
  flags : [-sr|-frz|-elf] [<path>|-tftp <path>|-serial] [-o <option>]
     -sr : S-Record / -frz : FRZ / -elf : ELF(exec type only) /
     <path> : file boot / -tftp <path> : tftp boot /
     -serial : serial boot / -o <option> : option
go <entry> [<arg1>] ..[<arg4>]    : execute function
reset                             : reset system

put <path>                        : TFTP put file
get <path>                        : TFTP get file
ping [<IP address>]               : send ICMP ECHO packets
ifconfig                          : show network configuration
syslog [<IP address>/off]         : control syslog

read <path> <addr>                : read file
write <path> <addr> <size>        : write file
ls [-a] <path>                    : list file
      -a : all file
rm [-r] <path>                    : remove file
      -r : recursive
cp [-r] <src_path> <dist_path>    : copy file
      -r : recursive
mv <src_path> <dist_path>         : move file
df                                : disk free
cd <path>                         : change directory
mkdir <path>                      : make directory
chmod <mode> <file>               : change mode
chown <user> <file>               : change owner
    <user> : [root/user]
ln <src> <dist>                   : symbolic link
mknod <file> <type> [<maj> <min>] : make special file
  <type> : [b|c|p|s]
format <device_path> [<flags>]    : format filesystem
  flags : -physical : physical format
          -partition <p0>[,<p1>][,<p2>][,<p3>]
               <pn> : partition size ratio
fsck <device_path>                : file system check

echo [-n] [<arg1>] .. [<argn>]    : print argument
wait                              : wait key
set [<environment>] [<value>]     : environment set
more <path>                       : show text file
pci                               : show PCI bus
version                           : show version
h[elp] | ?                        : show this message
```

