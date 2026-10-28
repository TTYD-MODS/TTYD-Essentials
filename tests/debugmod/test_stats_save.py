"""Exercise the mod's actual stat and save-start helpers with fake game state."""
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class StatsSaveTest(unittest.TestCase):
    def test_stat_bounds_and_save_guards(self):
        compiler = shutil.which('/Library/Developer/CommandLineTools/usr/bin/clang') or shutil.which('cc')
        if not compiler:
            self.skipTest('C compiler not available')
        source = (Path(__file__).parents[2] / 'mods/debug_menu.c').read_text()
        def function(name):
            return re.search(r'static (?:s32|void|BOOL) ' + name + r'\([^\n]*\) \{.*?\n\}', source, re.S).group()
        lifecycle_start = source.index('    if (debug_save_event) {')
        lifecycle_end = source.index('    if (seqGetSeq()', lifecycle_start)
        lifecycle = source[lifecycle_start:lifecycle_end]
        harness = r'''
#include <assert.h>
typedef int s32; typedef unsigned int u32;
typedef int BOOL;
#define FALSE 0
#define TRUE 1
#define EVENT_ACTIVE 1
static int debug_save_event, refreshes, level, save_script, save_active, polls_completed;
static u32 debug_stat_locks;
static s32 debug_locked_values[7];
static int *mobj_save_blk_sysevt = &save_script;
typedef struct {int currentHP, maximumHP, baseMaxHP, currentFP, maximumFP, baseMaxFP, maximumBP, availableBP, coins, mStarPieceCount;} PouchData;
typedef struct {int flags, eventId;} EventEntry;
typedef struct {int count; EventEntry *entries;} EventWork;
typedef struct {int systemLevelFlags;} GlobalWork;
static PouchData pouch = {5,15,10,2,10,5,10,4,50,1};
static EventEntry entries[5];
static EventWork work = {5, entries};
static GlobalWork global, *gp = &global;
static PouchData *pouchGetPtr(void) { return &pouch; }
static void pouchReviseMarioParam(void) { pouch.maximumHP=pouch.baseMaxHP+5; pouch.maximumFP=pouch.baseMaxFP+5; if(pouch.currentHP>pouch.maximumHP)pouch.currentHP=pouch.maximumHP; if(pouch.currentFP>pouch.maximumFP)pouch.currentFP=pouch.maximumFP; pouch.availableBP=pouch.maximumBP-6; }
static int pouchSetCoin(int n) { return pouch.coins=n; }
static void statusWinForceUpdate(void) { ++refreshes; }
static EventWork *evtGetWork(void) { return &work; }
static void marioStSystemLevel(int n) { level=n; global.systemLevelFlags=n; }
static int evtCheckID(int id) { assert(id == 77); return save_active; }
static EventEntry *evtEntryType(void *script, int priority, int flags, int type) { assert(script==mobj_save_blk_sysevt && priority==30 && flags==0 && type==26); entries[0].eventId=77; return &entries[0]; }
''' + '\n'.join(function(n) for n in ('debug_clamp', 'debug_read_stat', 'debug_change_stat', 'debug_start_save')) + '\nstatic void poll_save(void) {\n' + lifecycle + r'''
    ++polls_completed;
}
int main(void) {
    debug_change_stat(0, -100); assert(pouch.currentHP == 1);
    debug_change_stat(1, -100); assert(pouch.baseMaxHP == 1 && pouch.maximumHP == 6 && pouch.availableBP == 4);
    debug_change_stat(2, 100); assert(pouch.currentFP == pouch.maximumFP);
    debug_change_stat(3, -100); assert(pouch.baseMaxFP == 0 && pouch.maximumFP == 5 && pouch.currentFP == 5);
    debug_change_stat(4, -100); assert(pouch.maximumBP == 6 && pouch.availableBP == 0);
    debug_change_stat(5, 2000); assert(pouch.coins == 999);
    debug_change_stat(6, -100); assert(pouch.mStarPieceCount == 0);
    assert(refreshes == 7);
    global.systemLevelFlags=1; assert(!debug_start_save()); global.systemLevelFlags=0;
    entries[0].flags=1; entries[1].flags=1; assert(!debug_start_save());
    entries[0].flags=0; entries[1].flags=0; assert(debug_start_save());
    assert(level == 1 && debug_save_event == 77 && !debug_start_save());
    save_active=1; poll_save(); assert(level == 1 && debug_save_event == 77 && polls_completed == 0);
    save_active=0; poll_save(); assert(level == 0 && debug_save_event == 0 && polls_completed == 1);
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
