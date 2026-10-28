#!/usr/bin/env python3
"""Apply the G8ME01 state-menu patch to a separate copy of a user-owned ISO."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import sys
import zipfile

HOOKS = ((0x8006F928, 0x4BF966D1, "debug_input_hook"),
         (0x8006F9A4, 0x4BFEF0D9, "debug_draw_hook"),
         (0x8006F944, 0x4BF9FDC1, "debug_camera_hook"),
         (0x800FB480, 0x48002311, "debug_damage_hook"),
         (0x80295488, 0x480012C5, "debug_arena_lo_hook"),
         (0x802954C4, 0x48001289, "debug_arena_lo_hook"))


def word(data, offset):
    return struct.unpack_from(">I", data, offset)[0]


def put(data, offset, value):
    struct.pack_into(">I", data, offset, value)


def branch(source, target):
    delta = target - source
    if delta % 4 or not -0x02000000 <= delta < 0x02000000:
        raise ValueError("Hook target is outside PowerPC branch range")
    return 0x48000001 | (delta & 0x03FFFFFC)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("iso", type=Path, help="original US revision-0 G8ME01 ISO")
    parser.add_argument("output", type=Path, help="new patched ISO (must not already exist)")
    parser.add_argument("--diagnostic-no-hooks", action="store_true", help="reserve memory and load payload without activating the menu")
    parser.add_argument("--payload-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--patch", type=Path, help=".ttydpatch package containing payload and manifest")
    options = parser.parse_args()
    source = options.iso.resolve(strict=True)
    output = options.output.absolute()
    if output.exists() or source == output.resolve():
        raise ValueError("Output must be a new file separate from the original ISO")
    if options.patch:
        with zipfile.ZipFile(options.patch) as archive:
            if set(archive.namelist()) != {"payload.bin", "manifest.json"} or len(archive.namelist()) != 2:
                raise ValueError("Invalid patch package contents")
            if archive.getinfo("payload.bin").file_size > 0x7400 or archive.getinfo("manifest.json").file_size > 65536:
                raise ValueError("Patch package is too large")
            payload = archive.read("payload.bin")
            manifest = json.loads(archive.read("manifest.json"))
    else:
        payload = (options.payload_dir / "payload.bin").read_bytes()
        manifest = json.loads((options.payload_dir / "manifest.json").read_text())
    if manifest.get("format") != 1 or len(payload) != manifest["payload_size"] or hashlib.sha256(payload).hexdigest() != manifest["payload_sha256"]:
        raise ValueError("Payload or manifest is invalid")
    if manifest.get("payload_address") != 0x80439a00 or not 0 < len(payload) <= 0x7400:
        raise ValueError("Payload lies outside the reserved debugger stack space")
    if any(not 0x80439a00 <= manifest["hooks"][name] < 0x80439a00 + len(payload) for _, _, name in HOOKS):
        raise ValueError("Payload hook lies outside the payload")
    with source.open("rb") as f:
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(0)
        boot = f.read(0x440)
        if len(boot) != 0x440 or boot[:6] != b"G8ME01" or boot[6:8] != b"\0\0":
            raise ValueError("Expected a US G8ME01 disc 0, revision 0")
        dol, fst, fst_size = word(boot, 0x420), word(boot, 0x424), word(boot, 0x428)
        if dol + 0x100 > size or fst + fst_size > size or fst_size < 12 or fst_size > 16*1024*1024:
            raise ValueError("Invalid disc system offsets")
        f.seek(dol)
        header = bytearray(f.read(0x100))
        if word(header, 8) or word(header, 0x50) or word(header, 0x98):
            raise ValueError("Required DOL text slot is already in use")
        sections = [(word(header,i*4),word(header,0x48+i*4),word(header,0x90+i*4)) for i in range(7)]
        sections += [(word(header,0x1c+i*4),word(header,0x64+i*4),word(header,0xac+i*4)) for i in range(11)]
        length = max([0x100] + [offset+n for offset, _, n in sections if n])
        if dol + length > size or length > 32*1024*1024:
            raise ValueError("Invalid DOL section ranges")
        f.seek(dol)
        original = f.read(length)
        if hashlib.sha256(original).hexdigest() != manifest["original_dol_sha256"]:
            raise ValueError("Original DOL hash differs; use the supported unmodified US revision-0 image")
        f.seek(fst)
        table = f.read(fst_size)
        count = word(table,8)
        if word(table,0) >> 24 != 1 or count < 1 or count > fst_size // 12:
            raise ValueError("Invalid disc file table")
        files = []
        for index in range(1,count):
            tag, start, length_entry = struct.unpack_from(">III",table,index*12)
            if tag >> 24 == 0 and length_entry:
                if start + length_entry > size:
                    raise ValueError("Disc file lies outside image")
                files.append((start,start+length_entry))
        start = (max(fst+fst_size,dol+length)+31) & ~31
        for a,b in sorted(files):
            if b <= start: continue
            if a >= start + length + len(payload): break
            start = (b+31) & ~31
        if start + length + len(payload) > size or any(start < b and start+length+len(payload) > a for a,b in files):
            raise ValueError("No safe space for payload in disc filesystem padding")
        changes = []
        for address, expected, name in HOOKS:
            match = [(offset+address-base) for offset,base,n in sections if n and base <= address and address+4 <= base+n]
            if len(match) != 1 or word(original, match[0]) != expected:
                raise ValueError(f"Original hook mismatch at 0x{address:08x}")
            if not options.diagnostic_no_hooks or name == "debug_arena_lo_hook":
                changes.append((match[0],branch(address,manifest["hooks"][name])))
        put(header,8,length)
        put(header,0x50,manifest["payload_address"])
        put(header,0x98,len(payload))
        print(f"Verified G8ME01 revision 0; payload uses disc padding at 0x{start:x}.")
        created = False
        try:
            with output.open("xb") as target:
                created = True
                f.seek(0)
                shutil.copyfileobj(f,target,8*1024*1024)
                target.seek(0x420)
                target.write(struct.pack(">I", start))
                target.seek(start)
                target.write(original)
                target.seek(start)
                target.write(header)
                target.seek(start + length)
                target.write(payload)
                for position, instruction in changes:
                    target.seek(start + position)
                    target.write(struct.pack(">I",instruction))
            if output.stat().st_size != size:
                raise ValueError("Patched image size changed unexpectedly")
        except BaseException:
            if created: output.unlink(missing_ok=True)
            raise
    print(f"Patched ISO created: {output}")
    print("Original image was left untouched. Use a copy of your save when testing.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        print(f"Patch failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
