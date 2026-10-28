"""Exercise the actual destination guard against a small fake disc table."""
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class DestinationGuardTest(unittest.TestCase):
    def test_disc_presence_and_demo_geometry(self):
        compiler = (shutil.which('/Library/Developer/CommandLineTools/usr/bin/clang')
                    or shutil.which('cc'))
        if not compiler:
            self.skipTest('C compiler not available')
        source = (Path(__file__).parents[2] / 'mods/debug_menu.c').read_text()
        guard = re.search(r'static BOOL debug_destination_available\(const char\* map\) \{.*?\n\}', source, re.S).group()
        harness = r'''
#include <stdio.h>
#include <string.h>
#include <assert.h>
#define BOOL int
#define FALSE 0
static int DVDConvertPathToEntrynum(const char *path) {
    const char *files[] = {"/rel/gor.rel", "/m/gor_00/d", "/m/gor_01/d", "/rel/dmo.rel", "/rel/gon.rel", 0};
    for (int i = 0; files[i]; ++i) if (!strcmp(path, files[i])) return i;
    return -1;
}
''' + guard + r'''
int main(void) {
    assert(debug_destination_available("gor_00"));
    assert(!debug_destination_available("tst_00")); /* no module or map */
    assert(!debug_destination_available("gon_bt00")); /* module, no map */
    assert(debug_destination_available("dmo_00")); /* uses gor_01 geometry */
    return 0;
}
'''
        with tempfile.TemporaryDirectory() as tmp:
            cfile = Path(tmp) / 'test.c'
            exe = Path(tmp) / 'test'
            cfile.write_text(harness)
            args = [compiler, '-std=c11', '-Wall', '-Werror']
            sdk = Path('/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk')
            if compiler.startswith('/Library/Developer/CommandLineTools/') and sdk.exists():
                args += ['-isysroot', str(sdk)]
            subprocess.run(args + [str(cfile), '-o', str(exe)], check=True)
            subprocess.run([str(exe)], check=True)
