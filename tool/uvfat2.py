#!/usr/bin/env python3
#warning: slop

"""
Manual FAT16 extractor for Sony "UVFAT16" style images.

Standard tools (7-Zip, mtools, Linux vfat driver) auto-detect FAT width
(12/16/32) purely from cluster count, per the MS FAT spec. Some vendor
images (like this Sony one) use 16-bit FAT entries even though the
cluster count falls in the "should be FAT12" range. This script reads
the BPB to get geometry, then unconditionally treats FAT entries as
16-bit, ignoring the cluster-count heuristic.

Usage:
    python3 extract_fat16.py 1.bin output_dir/
"""

import sys
import os
import struct


def read_bpb(f):
    f.seek(0)
    boot = f.read(512)

    bpb = {}
    bpb['bytes_per_sector'] = struct.unpack_from('<H', boot, 0x0B)[0]
    bpb['sectors_per_cluster'] = boot[0x0D]
    bpb['reserved_sectors'] = struct.unpack_from('<H', boot, 0x0E)[0]
    bpb['num_fats'] = boot[0x10]
    bpb['root_entries'] = struct.unpack_from('<H', boot, 0x11)[0]
    total_sectors_16 = struct.unpack_from('<H', boot, 0x13)[0]
    bpb['sectors_per_fat'] = struct.unpack_from('<H', boot, 0x16)[0]
    total_sectors_32 = struct.unpack_from('<I', boot, 0x20)[0]
    bpb['total_sectors'] = total_sectors_16 if total_sectors_16 != 0 else total_sectors_32
    bpb['oem_id'] = boot[0x03:0x0B].decode('ascii', errors='replace')
    bpb['label'] = boot[0x2B:0x36].decode('ascii', errors='replace') if len(boot) >= 0x36 else ''
    fstype = boot[0x36:0x3E].decode('ascii', errors='replace')
    bpb['fs_type_label'] = fstype

    return bpb


def compute_layout(bpb):
    bps = bpb['bytes_per_sector']
    reserved = bpb['reserved_sectors']
    num_fats = bpb['num_fats']
    spf = bpb['sectors_per_fat']
    root_entries = bpb['root_entries']
    spc = bpb['sectors_per_cluster']

    fat_start_sector = reserved
    root_dir_start_sector = reserved + (num_fats * spf)
    root_dir_sectors = ((root_entries * 32) + (bps - 1)) // bps
    data_start_sector = root_dir_start_sector + root_dir_sectors

    return {
        'bps': bps,
        'fat_start_byte': fat_start_sector * bps,
        'root_dir_start_byte': root_dir_start_sector * bps,
        'root_dir_sectors': root_dir_sectors,
        'data_start_byte': data_start_sector * bps,
        'spc': spc,
        'cluster_size': spc * bps,
    }


def read_fat16_table(f, layout, bpb):
    f.seek(layout['fat_start_byte'])
    fat_bytes = f.read(bpb['sectors_per_fat'] * layout['bps'])
    num_entries = len(fat_bytes) // 2
    fat = struct.unpack('<%dH' % num_entries, fat_bytes[:num_entries * 2])
    return fat


def cluster_to_offset(cluster, layout):
    # cluster numbering starts at 2
    return layout['data_start_byte'] + (cluster - 2) * layout['cluster_size']


def sfn_checksum(sfn_11):
    """Standard checksum of the 11-byte 8.3 name, used to match LFN entries to their SFN."""
    chk = 0
    for b in sfn_11:
        chk = (((chk & 1) << 7) + (chk >> 1) + b) & 0xFF
    return chk


def parse_dir_entries(raw):
    entries = []
    pending_lfn = {}  # seq_num -> (text, checksum)
    i = 0
    while i < len(raw):
        entry = raw[i:i+32]
        if len(entry) < 32:
            break
        first_byte = entry[0]
        if first_byte == 0x00:
            break  # end of directory
        if first_byte == 0xE5:
            pending_lfn = {}
            i += 32
            continue  # deleted entry

        attr = entry[0x0B]
        if attr == 0x0F:
            # LFN entry
            seq = entry[0]
            seq_num = seq & 0x1F  # low 5 bits = sequence number (1-based)
            checksum = entry[13]
            chars = b''
            chars += entry[1:11]     # 5 chars UTF-16LE
            chars += entry[14:26]    # 6 chars UTF-16LE
            chars += entry[28:32]    # 2 chars UTF-16LE
            try:
                text = chars.decode('utf-16le', errors='ignore')
            except Exception:
                text = ''
            text = text.split('\x00')[0]
            text = text.replace('\uffff', '')
            pending_lfn[seq_num] = (text, checksum)
            i += 32
            continue

        name_raw = entry[0:8]
        ext_raw = entry[8:11]
        name = name_raw.decode('ascii', errors='replace').strip()
        ext = ext_raw.decode('ascii', errors='replace').strip()
        is_dir = bool(attr & 0x10)
        is_volume_label = bool(attr & 0x08)

        if is_volume_label and not is_dir:
            pending_lfn = {}
            i += 32
            continue

        if name.startswith('.') and not name.replace('.', '').strip():
            # '.' or '..' entries
            pending_lfn = {}
            i += 32
            continue

        cluster = struct.unpack_from('<H', entry, 0x1A)[0]
        size = struct.unpack_from('<I', entry, 0x1C)[0]

        crt_time_raw = struct.unpack_from('<H', entry, 0x0E)[0]
        crt_date_raw = struct.unpack_from('<H', entry, 0x10)[0]
        acc_date_raw = struct.unpack_from('<H', entry, 0x12)[0]
        wrt_time_raw = struct.unpack_from('<H', entry, 0x16)[0]
        wrt_date_raw = struct.unpack_from('<H', entry, 0x18)[0]

        sfn = name_raw + ext_raw
        expected_chk = sfn_checksum(sfn)

        long_name = None
        if pending_lfn:
            if all(chk == expected_chk for (_, chk) in pending_lfn.values()):
                ordered = ''.join(
                    pending_lfn[k][0] for k in sorted(pending_lfn.keys())
                )
                if ordered:
                    long_name = ordered
        pending_lfn = {}

        fname = name if not ext else f"{name}.{ext}"
        final_name = long_name if long_name else fname

        entries.append({
            'name': final_name,
            'attr': attr,
            'is_dir': is_dir,
            'cluster': cluster,
            'size': size,
            'crt_date': crt_date_raw,
            'crt_time': crt_time_raw,
            'acc_date': acc_date_raw,
            'wrt_date': wrt_date_raw,
            'wrt_time': wrt_time_raw,
        })
        i += 32
    return entries


def fat_datetime_to_unix(date_raw, time_raw):
    """Decode FAT date/time fields into a Unix timestamp (local time, no timezone in FAT)."""
    if date_raw == 0:
        return None
    year = 1980 + ((date_raw >> 9) & 0x7F)
    month = (date_raw >> 5) & 0x0F
    day = date_raw & 0x1F
    hour = (time_raw >> 11) & 0x1F
    minute = (time_raw >> 5) & 0x3F
    second = (time_raw & 0x1F) * 2

    if month == 0 or day == 0:
        return None
    try:
        import datetime
        dt = datetime.datetime(year, month, day, hour, minute, second)
        return dt.timestamp()
    except ValueError:
        return None


def read_cluster_chain(f, fat, start_cluster, layout, max_bytes=None):
    data = b''
    cluster = start_cluster
    visited = set()
    EOC_MIN = 0xFFF8  # FAT16 end-of-chain range
    BAD = 0xFFF7

    while True:
        if cluster in visited:
            print(f"    WARNING: cluster loop detected at {cluster}, stopping")
            break
        if cluster < 2:
            break
        if cluster >= EOC_MIN:
            break
        if cluster == BAD:
            print(f"    WARNING: bad cluster marker hit")
            break
        visited.add(cluster)

        offset = cluster_to_offset(cluster, layout)
        f.seek(offset)
        chunk = f.read(layout['cluster_size'])
        data += chunk

        if max_bytes is not None and len(data) >= max_bytes:
            break

        if cluster >= len(fat):
            print(f"    WARNING: cluster {cluster} out of FAT range, stopping")
            break

        cluster = fat[cluster]

    if max_bytes is not None:
        data = data[:max_bytes]
    return data


def apply_timestamps(path, e):
    """Set mtime/atime on the extracted file/dir from the FAT entry's write/access dates.
    FAT has no reliable timezone info, so times are applied as local wall-clock time."""
    wrt_ts = fat_datetime_to_unix(e['wrt_date'], e['wrt_time'])
    acc_ts = fat_datetime_to_unix(e['acc_date'], 0)  # FAT access date has no time component

    if wrt_ts is None:
        return  # nothing usable to set

    atime = acc_ts if acc_ts is not None else wrt_ts
    mtime = wrt_ts
    try:
        os.utime(path, (atime, mtime))
    except Exception as ex:
        print(f"    WARNING: could not set timestamps on {path}: {ex}")


def extract_dir(f, fat, layout, entries, out_dir, depth=0):
    os.makedirs(out_dir, exist_ok=True)
    dir_entries_to_stamp = []  # (path, entry) - apply after children are written,
                                # since writing children updates the dir's own mtime
    for e in entries:
        indent = '  ' * depth
        if e['is_dir']:
            print(f"{indent}[DIR] {e['name']}")
            sub_out = os.path.join(out_dir, e['name'])
            if e['cluster'] == 0:
                os.makedirs(sub_out, exist_ok=True)
                dir_entries_to_stamp.append((sub_out, e))
                continue
            sub_data = read_cluster_chain(f, fat, e['cluster'], layout)
            sub_entries = parse_dir_entries(sub_data)
            extract_dir(f, fat, layout, sub_entries, sub_out, depth + 1)
            dir_entries_to_stamp.append((sub_out, e))
        else:
            print(f"{indent}{e['name']}  ({e['size']} bytes, start cluster {e['cluster']})")
            out_path = os.path.join(out_dir, e['name'])
            if e['cluster'] == 0 and e['size'] == 0:
                # empty file
                open(out_path, 'wb').close()
                apply_timestamps(out_path, e)
                continue
            try:
                data = read_cluster_chain(f, fat, e['cluster'], layout, max_bytes=e['size'])
                with open(out_path, 'wb') as out:
                    out.write(data)
                if len(data) != e['size']:
                    print(f"{indent}  WARNING: expected {e['size']} bytes, got {len(data)}")
                apply_timestamps(out_path, e)
            except Exception as ex:
                print(f"{indent}  ERROR extracting {e['name']}: {ex}")

    # stamp directories last, so their own mtime isn't overwritten by child writes
    for sub_out, e in dir_entries_to_stamp:
        apply_timestamps(sub_out, e)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <image.bin> <output_dir>")
        sys.exit(1)

    img_path = sys.argv[1]
    out_dir = sys.argv[2]

    with open(img_path, 'rb') as f:
        bpb = read_bpb(f)
        print("=== BPB ===")
        for k, v in bpb.items():
            print(f"  {k}: {v}")

        layout = compute_layout(bpb)
        print("\n=== Layout ===")
        for k, v in layout.items():
            print(f"  {k}: {v}")

        print("\n=== Reading FAT (forced 16-bit entries) ===")
        fat = read_fat16_table(f, layout, bpb)
        print(f"  FAT entries: {len(fat)}")

        print("\n=== Root directory ===")
        f.seek(layout['root_dir_start_byte'])
        root_raw = f.read(layout['root_dir_sectors'] * layout['bps'])
        root_entries = parse_dir_entries(root_raw)

        print(f"\n=== Extracting to {out_dir} ===")
        extract_dir(f, fat, layout, root_entries, out_dir)

    print("\nDone.")


if __name__ == '__main__':
    main()