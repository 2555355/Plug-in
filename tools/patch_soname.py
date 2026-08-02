#!/usr/bin/env python3
"""Patch the DT_SONAME string in an ELF shared object.

Replaces the SONAME string in the .dynstr section. The new name must be
shorter than or equal to the old name so the remainder can be zero-padded
(ELF strings are NUL-terminated, so trailing NULs are harmless).
"""
import sys
import struct

def patch_soname(path, old_name, new_name):
    old_b = old_name.encode() + b'\x00'
    new_b = new_name.encode() + b'\x00'
    if len(new_b) > len(old_b):
        raise SystemExit(f"new name ({len(new_b)}) longer than old ({len(old_b)}); cannot patch safely")

    with open(path, 'rb') as f:
        data = bytearray(f.read())

    assert data[:4] == b'\x7fELF', "not an ELF file"
    ei_class = data[4]
    assert ei_class == 2, "only ELF64 supported"
    e_shoff = struct.unpack_from('<Q', data, 0x28)[0]
    e_shentsize = struct.unpack_from('<H', data, 0x3a)[0]
    e_shnum = struct.unpack_from('<H', data, 0x3c)[0]

    def sh(i):
        base = e_shoff + i * e_shentsize
        sh_type = struct.unpack_from('<I', data, base + 4)[0]
        sh_offset = struct.unpack_from('<Q', data, base + 24)[0]
        sh_size = struct.unpack_from('<Q', data, base + 32)[0]
        sh_link = struct.unpack_from('<I', data, base + 40)[0]
        return sh_type, sh_offset, sh_size, sh_link

    dyn_off = dyn_size = None
    dynstr_off = dynstr_size = None
    for i in range(e_shnum):
        sh_type, sh_offset, sh_size, sh_link = sh(i)
        if sh_type == 6:  # SHT_DYNAMIC
            dyn_off, dyn_size = sh_offset, sh_size
            ds_type, ds_off, ds_size, _ = sh(sh_link)
            assert ds_type == 3, "sh_link of .dynamic is not STRTAB"
            dynstr_off, dynstr_size = ds_off, ds_size
            break

    if dynstr_off is None:
        raise SystemExit("could not locate .dynstr via .dynamic")

    print(f".dynstr: offset=0x{dynstr_off:x} size=0x{dynstr_size:x}")

    soname_strtab_off = None
    if dyn_off is not None:
        n = dyn_size // 16
        for k in range(n):
            ent = dyn_off + k * 16
            d_tag = struct.unpack_from('<q', data, ent)[0]
            d_val = struct.unpack_from('<Q', data, ent + 8)[0]
            if d_tag == 14:  # DT_SONAME
                soname_strtab_off = d_val
                break
            if d_tag == 0:  # DT_NULL
                break

    if soname_strtab_off is None:
        raise SystemExit("DT_SONAME not found")

    abs_off = dynstr_off + soname_strtab_off
    current = bytes(data[abs_off:abs_off + len(old_b)])
    print(f"DT_SONAME strtab off = 0x{soname_strtab_off:x} (file off 0x{abs_off:x})")
    print(f"current bytes: {current!r}")
    if current != old_b:
        raise SystemExit(f"SONAME at that offset is {current!r}, expected {old_b!r}")

    data[abs_off:abs_off + len(old_b)] = new_b + b'\x00' * (len(old_b) - len(new_b))

    with open(path, 'wb') as f:
        f.write(data)

    print(f"patched SONAME: {old_name!r} -> {new_name!r} (zero-padded {len(old_b) - len(new_b)} bytes)")

if __name__ == '__main__':
    patch_soname(sys.argv[1], sys.argv[2], sys.argv[3])
