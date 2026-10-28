# TTYD Essentials

TTYD Essentials is an in-game state editor and exploration menu for the North American GameCube release of *Paper Mario: The Thousand-Year Door* (G8ME01, disc 0, revision 0). It applies a small patch to your own disc image for use with Dolphin; no game image, assets, or compiler binaries are included.

The current features have been playtested in Dolphin. They have not been exhaustively tested in every story state or on original hardware. Back up your memory card before changing progress or saving.

## Features

- Browse story events and warp to their associated maps, or apply an approximate story preset.
- Browse maps and available room entrances; destinations missing from the disc are blocked.
- Change characters and partner availability and upgrade ranks; dismiss the active partner.
- Edit and lock player stats, adjust partner health and battle damage modifiers, and use the game's save menu.
- Add or remove items and badges, and explore with a free camera and horizontal wall bypass.

Open or close the menu with **L + R + Z + Start**. See the [menu guide](mods/README.md) for controls, behavior, and limitations.

## Build and play

Download a release installer bundle when one is available, extract it, and follow its instructions to patch your own US revision 0 ISO. To build the patch from source or prepare a release, follow [BUILDING_MOD.md](BUILDING_MOD.md). The original image remains untouched. The patcher checks the game ID, revision, original executable, hook instructions, and payload before producing an image.

For implementation details and development lessons, see [modding notes](mods/MODDING_NOTES.md). The [flag index](docs/FLAG_INDEX.md) and [story-event index](docs/STORY_EVENTS.md) are source references, not complete semantic documentation of every game flag.

## Source and attribution

This repository builds on [LLCOOLT/ttyd](https://github.com/LLCOOLT/ttyd), pinned at commit `84d1001ce033f7998e118f62a8aa4835134f40ac`. The mod uses its headers and US symbol map from an external checkout when compiling; the full game source is not included in this repository. The upstream project credits [doldecomp/ttyd](https://github.com/doldecomp/ttyd), [NWPlayer123](https://github.com/NWPlayer123), and [Silver136](https://github.com/Silver-136/ttyd_dtk_Silver136). Mod research also used [TTYD Practice Codes](https://github.com/Zephiles/TTYD-Practice-Codes); see the modding notes for details. Preserve the included [LICENSE](LICENSE) and notices in dependencies.

The mod lives in `mods/`, its build and patch tools in `tools/debugmod/`, and tests in `tests/debugmod/`. The full game source and original build are available from upstream.
