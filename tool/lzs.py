#warning: slop

class LzsDecodeError(Exception):
    pass


def lzs_decompress(data: bytes,
                    uncompressed_size: int | None = None,
                    n: int = 4096, f: int = 18, threshold: int = 2,
                    fill_byte: int = 0x00):
    """
    Okumura-style LZSS decompression (ring-buffer variant),
    matching the Rust `decompress_internal`.

    Two modes, chosen automatically based on `uncompressed_size`:

    1. uncompressed_size is KNOWN (int):
         `data` may contain trailing bytes belonging to the NEXT section
         (checksum, next header, etc). Decoding stops as soon as
         `uncompressed_size` bytes have been produced, and the number of
         input bytes consumed is returned so the caller knows where the
         next section starts.

    2. uncompressed_size is None (unknown):
         `data` MUST be exactly the compressed bytes for this section
         (i.e. compressed_size is already known and you've sliced `data`
         to that length). Decoding runs until input is exhausted, exactly
         like the Rust loop's `reader.read() -> None` termination.

    Returns (decompressed_bytes, compressed_size_consumed).
    """
    buffer = bytearray([fill_byte]) * n
    r = n - f
    flags = 0

    pos = 0
    out = bytearray()

    def read_byte():
        nonlocal pos
        if pos >= len(data):
            return None
        b = data[pos]
        pos += 1
        return b

    know_size = uncompressed_size is not None

    while True:
        if know_size and len(out) >= uncompressed_size:
            break

        flags >>= 1

        if (flags & 0x100) == 0:
            c = read_byte()
            if c is None:
                break  # input exhausted -- case 2 terminates here
            flags = c | 0xFF00

        if flags & 1:
            c = read_byte()
            if c is None:
                break
            out.append(c)
            buffer[r] = c
            r = (r + 1) & (n - 1)
        else:
            c1 = read_byte()
            c2 = read_byte()
            if c1 is None or c2 is None:
                break

            i = c1 | ((c2 & 0xF0) << 4)
            j = (c2 & 0x0F) + threshold

            for k in range(j + 1):
                if know_size and len(out) >= uncompressed_size:
                    break  # clamp: don't overshoot known target size
                c = buffer[(i + k) & (n - 1)]
                out.append(c)
                buffer[r] = c
                r = (r + 1) & (n - 1)

    compressed_size = pos

    if know_size and len(out) != uncompressed_size:
        raise LzsDecodeError(
            f"expected {uncompressed_size} bytes, got {len(out)} "
            f"(input exhausted at offset {pos})"
        )

    return bytes(out), compressed_size