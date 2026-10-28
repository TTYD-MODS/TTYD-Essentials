"""Exercise the actual partner-level and dismissal helpers with fake game state."""
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class PartnerLevelTest(unittest.TestCase):
    def test_rank_cycle_and_preserve_story_follower(self):
        compiler = shutil.which('/Library/Developer/CommandLineTools/usr/bin/clang') or shutil.which('cc')
        if not compiler:
            self.skipTest('C compiler not available')
        source = (Path(__file__).parents[2] / 'mods/debug_menu.c').read_text()
        dismiss = re.search(r'static void debug_dismiss_partner\(void\) \{.*?\n\}', source, re.S).group()
        advance = re.search(r'static void debug_advance_partner\(PartyId id\) \{.*?\n\}', source, re.S).group()
        harness = r'''
#include <assert.h>
typedef int s32;
typedef int PartyId;
typedef struct { int HPLevel, attackLevel, techLevel, currentHP, maximumHP; } PouchPartyData;
typedef struct { PouchPartyData partyData[8]; } PouchData;
typedef struct { int currPartySlotId[2]; } MarioWork;
static MarioWork mario = {{3, 7}};
static PouchData pouch;
static int joined[8], active = 1, killed = -1;
static MarioWork *marioGetPtr(void) { return &mario; }
static PouchData *pouchGetPtr(void) { return &pouch; }
static int marioGetPartyId(void) { return active ? 3 : -1; }
static int marioGetParty(void) { return active; }
static void partyKill(int slot) { killed = slot; active = 0; }
static int partyChkJoin(int id) { return joined[id]; }
static void partyJoin(int id) { joined[id] = 1; }
static void partyLeft(int id) { joined[id] = 0; }
static void pouchRevisePartyParam(void) {
    for (int i=1; i<8; ++i) pouch.partyData[i].maximumHP = 10 + 5*pouch.partyData[i].HPLevel;
}
''' + dismiss + '\n' + advance + r'''
int main(void) {
    PouchPartyData *p = &pouch.partyData[1];
    debug_advance_partner(1);
    assert(joined[1] && p->HPLevel == 0 && p->attackLevel == 0 && p->techLevel == 0 && p->currentHP == 10);
    debug_advance_partner(1);
    assert(p->HPLevel == 1 && p->attackLevel == 1 && p->techLevel == 1 && p->currentHP == 15);
    debug_advance_partner(1);
    assert(p->HPLevel == 2 && p->attackLevel == 2 && p->techLevel == 2 && p->currentHP == 20);
    debug_advance_partner(1);
    assert(!joined[1] && killed == 3 && mario.currPartySlotId[0] == -1 && mario.currPartySlotId[1] == 7);
    killed = -1;
    debug_dismiss_partner();
    assert(killed == -1 && mario.currPartySlotId[1] == 7);
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
