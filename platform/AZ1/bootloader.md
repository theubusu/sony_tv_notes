# Bootloader
The bootloader used is Sony's ABK Monitor. Both dumps i have contain version M3.009C from Mar 30 2010, 20:18:31.

It contains support for networking, Memory sticks, Fat filesystem, AES.

For some reason, in NAND, each 0x4000 chunk of the bootloader is repeated twice. This is also the case in many older Sony TVs (for redundancy/recovery?). So you need to remove every second 0x4000 region to get the proper bootloader.

At the end of the bootloader region there is also a 0x1d80 chunk of data that varies per device. It looks like some garbage mostly filled by 0xff bytes.

## Analysis
The bootloader is mostly valid MIPS code, although it starts with seemingly some sort of header/address table and signature(s).   
My best guess for the load address is `0x8004ff80`. But even with the supposedly correct address, the decompilation is just very strange, strings are misaligned by random byte count, instructions are sometimes invalid, functions/addresses have no expected references, and the whole thing is just a big mess. I have no idea what the reason for this is, maybe I am doing something wrong. 

## Environment variables
My current theory is that the environment variables (cmdline, frzkey, serial..) come from the `.environment` file contained in the root. The file looks to be encrypted, and is probably decrypted using the AES support built into the bootloader using some unique key. Due to the decompilation issues described above, i wasn't able to confirm this.

## Obfuscated strings
At 0x31A94 there seems to be a block of strings that are XORed with 0xAA, they are mostly related to the security stuff:
- avoid_lock
- locked_by_rng
- media.auth
- frzkey
- serial
- authentication
- login
- password

## AES tables
AES tables found in the bootloader (https://github.com/exscape/AES/blob/master/tables.h)
```
31B58		gmul2
31C58		sbox
			gmul9
			gmul13
			gmul11
			gmul14
			gmul3
32258		invsbox
```

## Command table 
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

