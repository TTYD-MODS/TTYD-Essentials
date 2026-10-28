"""Check story event selection using the actual mod function."""
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class StorySelectorTest(unittest.TestCase):
    def test_exact_and_next_event(self):
        compiler = shutil.which('/Library/Developer/CommandLineTools/usr/bin/clang') or shutil.which('cc')
        if not compiler:
            self.skipTest('C compiler not available')
        source = (Path(__file__).parents[2] / 'mods/debug_menu.c').read_text()
        function = re.search(r'static EventData\* debug_story_event\(s32 value, BOOL next\) \{.*?\n\}', source, re.S).group()
        harness = r'''
#include <assert.h>
#include <stddef.h>
typedef int s32;
typedef int BOOL;
typedef struct { int id; } EventData;
typedef struct { EventData *data; int count; } EventStage;
static EventData entries1[] = {{0}, {4}, {4}, {20}};
static EventData entries2[] = {{10}, {30}};
static EventStage stages[] = {{entries1, 4}, {entries2, 2}};
static int eventStgNum(void) { return 2; }
static EventStage *eventStgDtPtr(int i) { return &stages[i]; }
''' + function + r'''
int main(void) {
  assert(debug_story_event(4, 0) == &entries1[1]);
  assert(debug_story_event(4, 1) == &entries2[0]);
  assert(debug_story_event(29, 1) == &entries2[1]);
  assert(debug_story_event(30, 1) == NULL);
  assert(debug_story_event(11, 0) == NULL);
  assert(debug_story_event(0, 2) == NULL);
  assert(debug_story_event(4, 2) == &entries1[0]);
  assert(debug_story_event(10, 2) == &entries1[3]); /* table order, not numeric order */
  assert(debug_story_event(11, 2) == NULL);
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
