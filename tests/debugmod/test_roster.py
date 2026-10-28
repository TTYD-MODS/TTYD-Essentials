"""Exercise the roster page input using fake game state."""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class RosterTest(unittest.TestCase):
    def test_character_and_partner_safeguards(self):
        compiler = shutil.which('/Library/Developer/CommandLineTools/usr/bin/clang') or shutil.which('cc')
        if not compiler:
            self.skipTest('C compiler not available')
        mod = (Path(__file__).parents[2] / 'mods/debug_menu.c').read_text()
        start = mod.index('        if (debug_page == 1) {')
        end = mod.index('        world = debug_world();', start)
        block = mod[start:end]
        harness = r'''
#include <assert.h>
typedef int PartyId;
typedef struct { int characterId; } MarioWork;
#define PAD_BUTTON_UP 1
#define PAD_BUTTON_DOWN 2
#define PAD_BUTTON_LEFT 4
#define PAD_BUTTON_RIGHT 8
#define PAD_BUTTON_A 16
#define PAD_BUTTON_B 32
#define PAD_TRIGGER_Z 64
static int debug_page=1, debug_row, debug_character, debug_open=1, debug_consume, active, joined[8], dismissed;
static MarioWork player;
static int debug_wrap(int n, int count) { return n < 0 ? count-1 : n >= count ? 0 : n; }
static MarioWork *marioGetPtr(void) { return &player; }
static int marioGetParty(void) { return active; }
static void marioSetCharMode(int mode) { player.characterId = mode; }
static void debug_advance_partner(PartyId id) { joined[id]++; }
static void debug_dismiss_partner(void) { active=0; dismissed++; }
static void press(unsigned pressed) {
    unsigned held = pressed, chord = 0x1c0;
''' + block + r'''
consume_buttons: ;
}
int main(void) {
    press(PAD_BUTTON_RIGHT); assert(debug_character == 1);
    active=1; press(PAD_BUTTON_A); assert(player.characterId == 0);
    active=0; press(PAD_BUTTON_A); assert(player.characterId == 1);
    press(PAD_BUTTON_DOWN); assert(debug_row == 1);
    press(PAD_BUTTON_A); assert(joined[1] == 1);
    press(PAD_BUTTON_A); assert(joined[1] == 2);
    active=1; press(PAD_TRIGGER_Z); assert(active == 0 && dismissed == 1);
    debug_row=7; press(PAD_BUTTON_DOWN); assert(debug_row == 0);
    press(PAD_BUTTON_B); assert(!debug_open && debug_consume);
    return 0;
}
'''
        with tempfile.TemporaryDirectory() as tmp:
            cfile, exe = Path(tmp) / 'test.c', Path(tmp) / 'test'
            cfile.write_text(harness)
            args = [compiler, '-std=c11', '-Wall', '-Werror']
            sdk = Path('/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk')
            if compiler.startswith('/Library/Developer/CommandLineTools/') and sdk.exists():
                args += ['-isysroot', str(sdk)]
            subprocess.run(args + [str(cfile), '-o', str(exe)], check=True)
            subprocess.run([str(exe)], check=True)
