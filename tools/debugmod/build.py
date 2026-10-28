#!/usr/bin/env python3
"""Build the address-stable G8ME01 mod payload from its source."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = 0x80439a00
NAMES = "sqrt atan2 sin cos BattleCalculateDamage BattleTransPartyId pouchEquipCheckBadge bero_get_BeroNUM bero_get_ptr itemDataTable msgSearch pouchGetItem pouchRemoveItem pouchCheckItem strncpy strlen marioKeyOffChk marioChgStayMotion marioChgShipMotion marioPartyKill marioPartyEntry swInit camMain camGetPtr evtGetWork evtCheckID evtEntryType marioStSystemLevel mobj_save_blk_sysevt statusWinForceUpdate pouchReviseMarioParam pouchSetCoin marioGetPartyId partyKill pouchGetPtr pouchRevisePartyParam marioGetPtr marioGetParty marioSetCharMode partyChkJoin partyJoin partyLeft mapDataPtr eventStgNum eventStgDtPtr DVDConvertPathToEntrynum OSSetArenaLo FontDrawColor FontDrawEdge FontDrawScale FontDrawStart FontDrawString _restgpr_26 _savegpr_26 _restgpr_21 _savegpr_21 _restgpr_29 _savegpr_29 _restgpr_28 _savegpr_28 _restgpr_27 _savegpr_27 _restgpr_23 _savegpr_23 _restgpr_22 _savegpr_22 _restgpr_24 _restgpr_25 _savegpr_24 _savegpr_25 dispEntry effMain gp makeKey seqCheckSeq seqGetSeq seqSetSeq sprintf strcmp swByteGet swByteSet swClear swGet swSet world_data".split()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", type=Path, required=True, help="checkout of LLCOOLT/ttyd at the documented revision")
    parser.add_argument("--tools", type=Path, required=True, help="directory containing wibo and sjiswrap.exe")
    parser.add_argument("--compilers", type=Path, required=True, help="compiler root containing GC/2.6/mwcceppc.exe")
    parser.add_argument("--binutils", type=Path, required=True, help="directory containing powerpc-eabi-{ld,objcopy,nm}")
    parser.add_argument("--output", type=Path, default=ROOT / "build/ttyd-essentials")
    opts = parser.parse_args()
    out = opts.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    upstream = opts.upstream.resolve(strict=True)
    tools, compilers, bins = opts.tools.resolve(), opts.compilers.resolve(), opts.binutils.resolve()
    obj, elf, payload = out / "menu.o", out / "payload.elf", out / "payload.bin"
    command = [str(tools / "wibo"), str(tools / "sjiswrap.exe"), str(compilers / "GC/2.6/mwcceppc.exe"),
               "-nodefaults", "-proc", "gekko", "-align", "powerpc", "-enum", "int", "-multibyte",
               "-char", "unsigned", "-fp", "hardware", "-Cpp_exceptions", "off", "-O4,p", "-inline", "auto",
               "-pragma", "warn_notinlined off", "-once", "-nosyspath", "-i", str(upstream / "include"), "-i", str(upstream / "libs/dolsdk2004/include"),
               "-i", str(upstream / "libs/dolsdk2004/include/libc"), "-i", str(upstream / "libs/musyx/include"), "-DVERSION_G8ME01", "-DSDK_REVISION=1",
               "-DNDEBUG=1", "-sdata", "0", "-sdata2", "0", "-lang=c", "-c", "mods/debug_menu.c", "-o", str(obj)]
    subprocess.run(command, cwd=ROOT, check=True)
    original = (upstream / "config/G8ME01/symbols.txt").read_text()
    lines = ["OUTPUT_ARCH(powerpc)", "ENTRY(debug_input_hook)"]
    for name in NAMES:
        match = re.search(r"^" + re.escape(name) + r"\s*=\s*\S+:(0x[0-9a-fA-F]+)", original, re.M)
        if not match:
            raise ValueError(f"Missing US symbol: {name}")
        lines.append(f"{name} = {match.group(1)};")
    lines.extend(["SECTIONS {", f"  . = 0x{BASE:x};",
                  "  .payload : ALIGN(32) { *(.text) *(.rodata) *(.data) *(.bss) }",
                  "  /DISCARD/ : { *(.mwcats*) *(.comment) }", "}"])
    script = out / "payload.ld"
    script.write_text("\n".join(lines) + "\n")
    subprocess.run([str(bins / "powerpc-eabi-ld"), "-T", str(script), "-o", str(elf), str(obj)], check=True)
    subprocess.run([str(bins / "powerpc-eabi-objcopy"), "-O", "binary", str(elf), str(payload)], check=True)
    listing = subprocess.check_output([str(bins / "powerpc-eabi-nm"), "-n", str(elf)], text=True)
    hooks = {}
    for name in ("debug_input_hook", "debug_draw_hook", "debug_arena_lo_hook", "debug_camera_hook", "debug_damage_hook"):
        match = re.search(r"^([0-9a-fA-F]+)\s+\w\s+" + name + r"$", listing, re.M)
        if not match:
            raise ValueError(f"Missing payload hook: {name}")
        hooks[name] = int(match.group(1), 16)
    data = payload.read_bytes()
    data += b"\0" * ((-len(data)) % 32)
    payload.write_bytes(data)
    if not data or len(data) > 0x7400 or not all(BASE <= address < BASE + len(data) for address in hooks.values()):
        raise ValueError("Payload or hooks exceed the reserved memory region")
    manifest = {"format": 1, "game_id": "G8ME01", "revision": 0,
                "original_dol_sha256": "93c79aa312ca57c2785d0854a516c554e7683b525f8c3456dad568f4c440451a",
                "payload_address": BASE, "payload_size": len(data),
                "payload_sha256": hashlib.sha256(data).hexdigest(), "hooks": hooks}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built {len(data)}-byte debug payload in {out}")


if __name__ == "__main__":
    main()
