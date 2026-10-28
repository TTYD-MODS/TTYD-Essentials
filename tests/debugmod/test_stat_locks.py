"""Exercise actual stat-lock functions against fake pouch and sequence state."""
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class StatLockTest(unittest.TestCase):
    def test_restore_badge_limits_and_session_reset(self):
        compiler = shutil.which('/Library/Developer/CommandLineTools/usr/bin/clang') or shutil.which('cc')
        if not compiler:
            self.skipTest('C compiler not available')
        source = (Path(__file__).parents[2] / 'mods/debug_menu.c').read_text()
        def function(name):
            return re.search(r'static (?:s32|void|BOOL) ' + name + r'\([^\n]*\) \{.*?\n\}', source, re.S).group()
        harness = r'''
#include <assert.h>
typedef int s32; typedef unsigned u32; typedef int BOOL;
#define TRUE 1
#define FALSE 0
#define SEQ_LOGO 0
#define SEQ_TITLE 1
#define SEQ_GAME 2
#define SEQ_BATTLE 4
static u32 debug_stat_locks;
static s32 debug_locked_values[7];
typedef struct {int currentHP, maximumHP, baseMaxHP, currentFP, maximumFP, baseMaxFP, maximumBP, availableBP, coins, mStarPieceCount;} PouchData;
static PouchData pouch = {5,15,10,2,10,5,10,4,50,1};
static int sequence=SEQ_GAME, badge_cost=6, refreshes;
static PouchData *pouchGetPtr(void) { return &pouch; }
static int seqGetSeq(void) { return sequence; }
static void pouchReviseMarioParam(void) { pouch.maximumHP=pouch.baseMaxHP+5; pouch.maximumFP=pouch.baseMaxFP+5; if(pouch.currentHP>pouch.maximumHP)pouch.currentHP=pouch.maximumHP; if(pouch.currentFP>pouch.maximumFP)pouch.currentFP=pouch.maximumFP; pouch.availableBP=pouch.maximumBP-badge_cost; }
static int pouchSetCoin(int n) { return pouch.coins=n; }
static void statusWinForceUpdate(void) { ++refreshes; }
''' + '\n'.join(function(n) for n in ('debug_clamp', 'debug_read_stat', 'debug_change_stat', 'debug_apply_stat_locks')) + r'''
int main(void) {
    debug_stat_locks=32; debug_locked_values[5]=50; pouch.coins=5;
    debug_apply_stat_locks(); assert(pouch.coins==50 && refreshes==1);
    debug_change_stat(5, 10); assert(pouch.coins==60 && debug_locked_values[5]==60);
    pouch.coins=900; sequence=3; debug_apply_stat_locks(); assert(pouch.coins==900);
    sequence=SEQ_GAME; debug_apply_stat_locks(); assert(pouch.coins==60);
    debug_stat_locks=1|2|4|8|16; debug_locked_values[0]=15; debug_locked_values[1]=10;
    debug_locked_values[2]=10; debug_locked_values[3]=5; debug_locked_values[4]=10;
    pouch.baseMaxHP=5; pouch.baseMaxFP=2; pouch.currentHP=1; pouch.currentFP=0;
    pouch.maximumBP=20; pouch.availableBP=2; badge_cost=18;
    debug_apply_stat_locks();
    assert(pouch.baseMaxHP==10 && pouch.maximumHP==15 && pouch.currentHP==15);
    assert(pouch.baseMaxFP==5 && pouch.maximumFP==10 && pouch.currentFP==10);
    assert(pouch.maximumBP==18 && pouch.availableBP==0);
    sequence=SEQ_TITLE; debug_apply_stat_locks(); assert(debug_stat_locks==0);
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
