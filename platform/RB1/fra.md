# FRA file format

The FRA file format (evolution of FRZ?) is a file format used for storing and executing data in sections mapped to memory adresses. The data is encrypted and verified, and can be additionally compressed.

It is used for the main linux image `vmlinux.fra` and `ssboot.fra`, and also for encrypting software packages.

## Structure
See `tool/fra.py`

FRA file consists of:

### File header (Not encrypted)
```
== File header: 0x80
[u8;16]		MagicCode; f4f18293 229ee954 a99d79d5 75db6c60
u32			TmpBufAddr
u32			FileHeaderSize
u32			SectionHeaderSize
u32			PayloadSize
u32			SectionHeader
u32			SecurityHeaderSize
[u8;8]		Reserved1
[u8;16]		SectionHeaderMAC
[u8;16]		InitialVector
[u8;16]		ReleaseKey
[u8;16]		PackageMAC
[u8;16]		Reserved2
```
Then follows SectionHeaderSize of encrypted section headers

### Section block header (Encrypted)
```
== Section Block header: 0x80
u32			SectionNum
u32			EntryPoint
u32			FileType
u32			BuildTime
[u8;16]		BuilderUID
[u8;32]		BuilderMailAddr
[u8;16]		BuilderMAC
u32         Machine
```
Follows SectionNum of Section headers (inside of the decrypted region)

### Section header (Encrypted)
```
== Section header: 0x80
u32			PayloadOffset
u32			PayloadSize
u32			Records
u32			SectionType
u32			MemoryAddress
u32			MemorySize
u32			AreaSize
u32			SubEntryPoint
[u8;16]		Reserved
[u8;16]		SectionMAC
[u8;16]		InitialVector
[u8;16]		Reserved2
```

Then follows `SecurityHeaderSize` of optional encrypted security header, its format is not known. Then the payload data follows.

## Encryption&Verification
FRA decryption is done fully using hardware crypto processor. That means it is not possible to decrypt their data outside the TV (unless you somehow get the master keys and process from it). The decryption also depends on the `EMK` environment value and `ReleaseKey`+`InitialVector` from the file's header

In `sonyrd.ko` the responsible function is `decrypt_data`. You can hook it from another kernel module and give it arbitrary data to decrypt, which is what i did (see `tool/decsrv`).

After decrypting the data is also compared to the stored CMAC and verified on the hardware side. You can however just ignore that step if you hook the direct decrypting function.

## Compression
Compressed sections utilize raw DEFLATE compression, which is also carried out by the hardware, so they have it accelerated.