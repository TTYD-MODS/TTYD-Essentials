"""Verify the target compiler reads atan2 results from the floating-point register."""
import os
import re
import subprocess
import unittest
from pathlib import Path


class CameraCodegenTest(unittest.TestCase):
    def test_target_atan2_return_abi(self):
        build_dir = os.environ.get('TTYD_DEBUGMOD_BUILD_DIR')
        objdump = os.environ.get('TTYD_DEBUGMOD_OBJDUMP')
        if not build_dir or not objdump:
            self.skipTest('Set TTYD_DEBUGMOD_BUILD_DIR and TTYD_DEBUGMOD_OBJDUMP to check a target build')
        elf = Path(build_dir) / 'payload.elf'
        disassembly = subprocess.check_output([objdump, '-d', str(elf)], text=True)
        start = disassembly.index('<debug_freecam_start>:')
        end = disassembly.index('<debug_freecam_move>:', start)
        section = disassembly[start:end]
        calls = list(re.finditer(r'\bbl\s+[^\n]*<atan2>[^\n]*\n', section))
        self.assertEqual(len(calls), 2)
        for call in calls:
            following = '\n'.join(section[call.end():].splitlines()[:6])
            self.assertRegex(following, r'\b(?:frsp|fmr|stfs)\s+f\d+,\s*f?1\b|\bstfs\s+f1,')
            self.assertNotRegex(following, r'\bxoris\s+r3,\s*r3')
