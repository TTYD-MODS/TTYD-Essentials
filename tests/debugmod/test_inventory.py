"""Exercise the inventory page's item bounds and operation dispatch."""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class InventoryPageTest(unittest.TestCase):
    def test_inventory_controls(self):
        compiler = shutil.which('/Library/Developer/CommandLineTools/usr/bin/clang') or shutil.which('cc')
        if not compiler:
            self.skipTest('C compiler not available')
        source = (Path(__file__).parents[2] / 'mods/debug_menu.c').read_text()
        start = source.index('        if (debug_page == 6) {')
        end = source.index('        if (debug_page == 5) {', start)
        block = source[start:end]
        harness = r'''
#include <assert.h>
typedef int s32; typedef int ItemType;
typedef struct {int mShineSpriteCount;} PouchData;
#define BADGE_MIN 0xf0
#define BADGE_MAX 0x153
#define ITEM_MAX 0xec
#define PAD_BUTTON_UP 1
#define PAD_BUTTON_DOWN 2
#define PAD_BUTTON_RIGHT 4
#define PAD_BUTTON_LEFT 8
#define PAD_BUTTON_Y 16
#define PAD_BUTTON_X 32
#define PAD_BUTTON_A 64
#define PAD_BUTTON_B 128
static int debug_page=6, debug_row, debug_item_kind, debug_item_id=0x80, debug_item_status, debug_open=1, debug_consume;
static int added, removed, revised_mario, revised_party;
static PouchData pouch;
static int debug_wrap(int n, int count) { return n<0 ? count-1 : n>=count ? 0 : n; }
static int debug_clamp(int n, int low, int high) { return n<low ? low : n>high ? high : n; }
static PouchData *pouchGetPtr(void) { return &pouch; }
static void statusWinForceUpdate(void) {}
static int pouchGetItem(ItemType id) { added=id; return 1; }
static int pouchRemoveItem(ItemType id) { removed=id; return 1; }
static void pouchReviseMarioParam(void) { revised_mario++; }
static void pouchRevisePartyParam(void) { revised_party++; }
static void press(unsigned pressed, unsigned held) {
    int direction, step;
''' + block + r'''
consume_buttons: ;
}
int main(void) {
    press(PAD_BUTTON_RIGHT,PAD_BUTTON_RIGHT); assert(debug_item_kind==1 && debug_item_id==BADGE_MIN);
    debug_row=1; press(PAD_BUTTON_LEFT,PAD_BUTTON_LEFT); assert(debug_item_id==BADGE_MIN);
    press(PAD_BUTTON_RIGHT,PAD_BUTTON_RIGHT|PAD_BUTTON_Y); assert(debug_item_id==BADGE_MAX-1);
    debug_row=2; press(PAD_BUTTON_A,PAD_BUTTON_A); assert(added==BADGE_MAX-1 && debug_item_status==1);
    debug_row=3; press(PAD_BUTTON_A,PAD_BUTTON_A); assert(removed==BADGE_MAX-1 && revised_mario==1 && revised_party==1);
    debug_row=4; pouch.mShineSpriteCount=999; press(PAD_BUTTON_RIGHT,PAD_BUTTON_RIGHT); assert(pouch.mShineSpriteCount==999);
    press(PAD_BUTTON_LEFT,PAD_BUTTON_LEFT|PAD_BUTTON_X); assert(pouch.mShineSpriteCount==989);
    press(PAD_BUTTON_B,PAD_BUTTON_B); assert(!debug_open && debug_consume);
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
