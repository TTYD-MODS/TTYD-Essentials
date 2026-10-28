"""Exercise the real story-warp input block with a fake event and disc."""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class StoryWarpTest(unittest.TestCase):
    def test_button_and_destination_guards(self):
        compiler = shutil.which('/Library/Developer/CommandLineTools/usr/bin/clang') or shutil.which('cc')
        if not compiler:
            self.skipTest('C compiler not available')
        mod = (Path(__file__).parents[2] / 'mods/debug_menu.c').read_text()
        start = mod.index('        if ((pressed & PAD_TRIGGER_Z) && debug_row == 0')
        end = mod.index('        if ((pressed & PAD_BUTTON_A) && debug_row == 3)', start)
        block = mod[start:end]
        harness = r'''
#include <assert.h>
#include <string.h>
typedef struct { int id; const char *mapName, *beroName; } EventData;
#define PAD_TRIGGER_Z 0x10
#define PAD_BUTTON_A 0x100
#define SEQ_MAP_CHANGE 3
#define FALSE 0
static int debug_row, debug_open, debug_consume, available, map_exists, sequence_calls;
static EventData test_event = {4, "gor_00", "s_bero"};
static EventData prev_event = {3, 0, 0};
static int progress = 4;
static EventData *debug_story_event(int value, int next) { return value == 4 ? (next == 2 ? &prev_event : &test_event) : 0; }
static int swByteGet(int index) { (void)index; return progress; }
static void swByteSet(int index, int value) { (void)index; progress = value; }
static int mapDataPtr(const char *name) { (void)name; return map_exists; }
static int debug_destination_available(const char *name) { (void)name; return available; }
static void seqSetSeq(int seq, const char *map, const char *entrance) {
    assert(seq == SEQ_MAP_CHANGE && !strcmp(map, "gor_00") && !strcmp(entrance, "s_bero"));
    ++sequence_calls;
}
static void press(unsigned pressed, unsigned held) {
    const unsigned chord = 0x70;
''' + block + r'''
}
int main(void) {
    debug_open = available = map_exists = 1;
    press(PAD_TRIGGER_Z, PAD_TRIGGER_Z);
    assert(sequence_calls == 1 && !debug_open && debug_consume && progress == 3);
    progress = 4;
    debug_open = 1; debug_consume = 0; available = 0;
    press(PAD_TRIGGER_Z, PAD_TRIGGER_Z);
    assert(sequence_calls == 1 && debug_open && !debug_consume && progress == 4);
    available = 1; map_exists = 0;
    press(PAD_TRIGGER_Z, PAD_TRIGGER_Z);
    assert(sequence_calls == 1 && debug_open);
    map_exists = 1;
    press(PAD_TRIGGER_Z, 0x70);
    assert(sequence_calls == 1 && debug_open);
    debug_row = 1;
    press(PAD_TRIGGER_Z, PAD_TRIGGER_Z);
    assert(sequence_calls == 1 && debug_open);
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
