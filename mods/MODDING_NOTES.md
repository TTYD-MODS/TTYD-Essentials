# TTYD Essentials development notes

These notes describe the implementation, test evidence, and limitations of TTYD Essentials. The repository is based on LLCOOLT/ttyd commit `84d1001ce033f7998e118f62a8aa4835134f40ac`. Generated images, game data, and compiler binaries are not included.

The current features have been playtested in Dolphin, including the corrected free camera. Testing is not exhaustive, and original-hardware compatibility is unverified.

## Rebuild and verify

Follow [BUILDING_MOD.md](../BUILDING_MOD.md) for setup, build, patch, and verification commands. Compiler and binutils locations are specific to each developer's environment.

The output image must not already exist. The compiler and game image are not shipped. `build.py` compiles `mods/debug_menu.c` with the original GC 2.6 compiler through wibo/sjiswrap, resolves addresses using the external upstream checkout's `config/G8ME01/symbols.txt`, and links a standalone payload with PowerPC binutils. The patcher verifies disc ID/revision, the original DOL SHA-256 (`93c79aa312ca57c2785d0854a516c554e7683b525f8c3456dad568f4c440451a`), original hook instructions, and payload hash; it creates a separate image. A successful build or unit test is not gameplay proof. The current build passed all 17 tests, including target-code ABI inspection; playtesting confirmed the camera fix.

`--diagnostic-no-hooks` creates a diagnostic image with startup arena hooks retained but the menu, camera, and damage hooks disabled. Read `tools/debugmod/patch.py` before relying on it: it is intended for isolating memory/loading problems, not as a playable menu.

## Executable and memory strategy

Rebuilding and relinking the base DOL with added game code shifts addresses referenced by the original RELs. This mod instead retains the original executable's addresses, injects an independent payload, and replaces selected original branch-and-link instructions. Each hook's original word is checked. The patcher copies the original DOL into unreferenced disc filesystem padding, adds a text section, redirects the disc header to the relocated DOL, and appends a 32-byte-aligned payload. It does not overwrite the source ISO or distribute a game binary.

The current payload starts at `0x80439a00` and is bounded to `0x7400` bytes; the startup hooks keep the arena floor at or above `0x80441000`. The tested payload is 27,904 bytes and ends at `0x80440700`, below that floor. This uses the reserved MetroTRK debugger-stack region and part of the original heap. Do not use this mod with MetroTRK active. Memory reservations and map/battle behavior need continued playtesting, especially on original hardware. Raising the arena floor reduces the game's available heap; never expand it blindly.

Current hook sites in `tools/debugmod/patch.py`:

| Address | Purpose |
| --- | --- |
| `0x8006f928` | Wrap `makeKey` and process menu input. |
| `0x8006f9a4` | Wrap `effMain`, apply stat/partner HP overrides, and enqueue menu drawing. |
| `0x8006f944` | Wrap `camMain` for free-camera control. |
| `0x800fb480` | Wrap the `BattleCalculateDamage` call used by `BattleCheckDamage`. |
| `0x80295488`, `0x802954c4` | Reserve payload memory through the two OS initialization arena-low calls. |

The initial `0x81700000` payload location hung in the apploader. A relocated original DOL with no payload was reported to work, so relocation alone was not the cause. A payload at `0x80439a00` without a sufficient arena reservation produced an unknown-instruction error at the first menu hook; OS startup can lower and clear the arena over that region, making payload erasure the leading explanation. Reserving the region allowed v6 to run. An earlier larger reservation had a reported graphics error and loading hang; one later accelerated playtest crashed, while the same diagnostic ran at normal speed. The underlying cause of the earlier hangs remains unconfirmed.

## Camera and collision lessons

The free camera temporarily suppresses the 3D camera callback during `camMain`, uses its own position and target, then restores the callback. It disables itself during map transitions and lets the game resume camera control. Controller input is captured before it is suppressed for the player. Movement is horizontal relative to camera yaw; L/R move vertically and the C-stick aims. Exploration-page speed is adjustable.

The v22 downward snap and lost horizontal aim were caused by the bundled GameCube `math.h` omitting an `atan2` declaration. Metrowerks implicitly assumed an integer return and read `r3`, although the game function returns a double in `f1`. The host C tests did not catch this because the host math header declared it correctly. `mods/debug_menu.c` now explicitly declares `double atan2(double, double)`; inspect target disassembly after future compiler or declaration changes. `test_camera_codegen.py` checks that both calls consume the floating-point return. The correction was confirmed in playtesting. This is a general lesson: check declarations and target calling conventions, not only host-side tests.

Wall-pass uses Mario's `0x400` horizontal movement flag, cross-checked against the game's movement code and [TTYD Practice Codes](https://github.com/Zephiles/TTYD-Practice-Codes). It leaves normal ground checks in place; it does not create a floor over gaps. The mod tracks whether it set the bit and avoids clearing it during Vivian's hide motion. Other mechanics may also use that flag; it is not a universal collision override. Wall-pass retains normal floor checks and needs additional testing across unusual game states.

Dolphin 2609a produced Metal shader errors involving `rawtex0` during testing. The dumped shader referenced it in a helper while declaring it inside `main`, consistent with a shader-generation issue; whether the mod triggers it or the unmodified game also does is unconfirmed. Switching the backend to OpenGL was suggested as an unverified workaround. The workaround has not been verified.

## Game state, maps, and inventory

- `GSW(0)` is the raw story sequence value, not a complete game state. The upstream game's event tables (`src/event.c`, `include/event.h`) provide English event names, map IDs, entrances, partners, and optional initialization callbacks. Some IDs repeat and one section is out of numeric order. A story warp chooses the first table entry for an ID and sets progress to the preceding **table entry**, matching the game's E3 sequence; this allows the selected event to run rather than loading its completed state. Other flags can still make a room appear completed.
- The story-preset page is a separate, double-confirmed destructive operation. It runs the game's E3-style event initializers through the selected entry, resets saved-work flags and pouch/partners, and warps. It is a debug approximation, not a verified normal-play snapshot. `pouchInit` allocates a new pouch without freeing the old one; repeated presets can leak game memory. Restart after repeated use and back up the memory card before testing.
- The original US disc's map list includes test maps that have no corresponding `/rel/tst.rel` or `/m/tst_*/d` files. They cannot be enabled by a story flag. The mod checks the current disc's FST for the area REL and map geometry before warping; `dmo_00` is the game's special case using `gor_01` geometry. This check does not establish that story flags, scripts, or spawn points are safe.
- The game exposes named `BeroEntry` entrances only for the **currently loaded room**. The entrance page lists that room's entrances; load a different room first to list its entrances. A selected name is copied into mod-owned memory before transition because unloading a REL can invalidate the original pointer. Names are raw game identifiers, not a fully researched map guide.
- The inventory page uses `pouchGetItem`, `pouchRemoveItem`, and `pouchCheckItem` for ordinary items and badges; removing a badge recalculates Mario and partner stats. It deliberately excludes key-item editing. Star Pieces are on Stats / Save and Shine Sprites on Inventory. Read `mods/README.md` before extending item ranges: some numeric IDs have immediate effects rather than behaving like held items.
- `mods/FLAGS.md` contains reviewed descriptions for 31 flags. `docs/FLAG_INDEX.md` is a generated literal-reference index, not a semantic dictionary; many of the 8,192 possible bits remain undocumented and dynamic references are missed. `docs/STORY_EVENTS.md` lists the 496 entries parsed from the event table. Regenerate with `tools/debugmod/index_flags.py /path/to/upstream` and `tools/debugmod/index_story.py /path/to/upstream` after source changes.

## Characters, stats, and saving

The character page calls the game's `marioSetCharMode`; it refuses switching to Peach or Bowser while a partner is active. The partner page sets availability and normal/super/ultra ranks using the game's pouch fields and parameter-recalculation routine. Z dismisses the active partner while preserving a separate story follower. Normal rank changes restore the partner's HP, matching `unitwin_setpartylank` in `src/event/evt_win.c`. Characters and partners outside their usual story context may have unexpected behavior.

The stats page changes current HP/FP, base maximum HP/FP, total BP, coins, and Star Pieces. Maximums account for badges; BP cannot be reduced below the equipped badge cost. Z locks a selected value; menu edits update the locked target. Locks restore pouch values per frame, persist across map transitions, and clear at the title/logo screen. Some battle systems maintain separate live values, so battle HP/FP are not guaranteed to remain locked.

The Character Stats page exposes per-character HP and **flat damage bonus/reduction**, not intrinsic attack or defense attributes. The hook adjusts positive HP damage returned by the normal `BattleCalculateDamage` call in `BattleCheckDamage`; it leaves zero/immune results, healing, FP damage, and scripted or other bypass paths alone. Modifiers clear at title/logo. Partner maximum-HP overrides are session controls; saved pouch data may retain values until recalculated. The battle hook has unit coverage; behavior in every battle situation has not been exhaustively verified.

Save Game starts the original `mobj_save_blk_sysevt` and normal memory-card confirmation flow. It checks event-slot availability and system level, pauses ordinary events, and restores the system level after the event completes. This is not yet proof that saving from arbitrary maps, story events, or character states reloads safely. Back up memory cards before testing.
