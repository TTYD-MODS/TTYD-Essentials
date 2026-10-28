# Building and releasing TTYD Essentials

## Apply a release

Download and extract the release installer ZIP. With Python 3 installed, run:

```sh
python3 apply.py /path/to/original-us.iso /path/to/TTYD-Essentials.iso \
  --patch TTYD-Essentials.ttydpatch
```

The input must be an unmodified North American GameCube ISO (G8ME01, disc 0, revision 0). Compressed Dolphin formats are not supported. The output must not already exist. The installer validates the game ID, revision, original executable hash, hook instructions, and patch payload; it leaves the input unchanged. Open the output ISO in Dolphin. Back up your memory card before changing game state.

## Build from source

Requirements: Python 3, a host C compiler for tests, and the GameCube tools used by the upstream project. The tool directory must contain `wibo` and `sjiswrap.exe`; the compiler directory must contain `GC/2.6/mwcceppc.exe`; the binutils directory must contain `powerpc-eabi-ld`, `powerpc-eabi-objcopy`, `powerpc-eabi-nm`, and, for the optional target test, `powerpc-eabi-objdump`.

Obtain a separate checkout of [LLCOOLT/ttyd](https://github.com/LLCOOLT/ttyd) at commit `84d1001ce033f7998e118f62a8aa4835134f40ac`. The build reads its headers and US symbol map; this repository does not contain the full game source. Its [build instructions](https://github.com/LLCOOLT/ttyd/blob/84d1001ce033f7998e118f62a8aa4835134f40ac/README.md) describe its dependencies. The mod build was verified on macOS with an existing local toolchain. The helper requires a `wibo` executable; compatibility on other hosts is unverified.

```sh
python3 tools/debugmod/build.py \
  --upstream /path/to/ttyd-upstream \
  --tools /path/to/tools \
  --compilers /path/to/compilers \
  --binutils /path/to/binutils \
  --output build/ttyd-essentials
```

## Create release artifacts

```sh
python3 tools/debugmod/package.py \
  --payload-dir build/ttyd-essentials \
  --output dist/TTYD-Essentials.ttydpatch \
  --bundle dist/TTYD-Essentials-release.zip
```

Both output paths must be new. The patch contains the mod payload and its manifest. The installer ZIP contains that patch, the Python installer, and instructions; neither artifact contains the original DOL, an ISO, or game assets. The `.ttydpatch` also works with the repository's `tools/debugmod/patch.py --patch` option.

To publish a release after pushing the repository to GitHub, create and push a version tag:

```sh
git tag v1.0.0
git push origin v1.0.0
```

The release workflow checks out the pinned upstream source, downloads the upstream project's pinned toolchain, builds the payload, runs the tests, and publishes both files as GitHub release assets. It requires GitHub Actions to be enabled and permission for the workflow to write repository contents. No original game image is needed by the workflow. The workflow uses a GitHub-hosted macOS Intel runner; it has not yet been verified in a live GitHub run. If a release already exists for the tag, the publishing step fails instead of replacing its assets.

## Tests

```sh
python3 -m unittest discover -s tests/debugmod -v
```

Set `TTYD_UPSTREAM` to the checkout path to enable checks against game source. After building, set `TTYD_DEBUGMOD_BUILD_DIR` to the output directory and `TTYD_DEBUGMOD_OBJDUMP` to `powerpc-eabi-objdump` to check the target compiler's camera calling convention. Without those inputs the relevant checks are skipped. These tests do not replace gameplay testing.

## Troubleshooting

- A disc or executable hash error means the input is not the expected unmodified US revision 0 image; use the correct original, not an already patched image.
- An existing-output error protects prior files. Choose a new filename or remove an unwanted generated copy yourself.
- A missing tool or source error means the supplied path does not contain the required files. Check the tool paths and upstream revision.
- Some maps, story transitions, or unusual character and progress combinations can be unstable. The mod uses the MetroTRK debugger-stack region, so do not use it with MetroTRK active.
