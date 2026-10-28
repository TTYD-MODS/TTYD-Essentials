"""Check release packages without requiring game data or a compiler."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile


class PackageTest(unittest.TestCase):
    def test_package_and_existing_output_guard(self):
        tool = Path(__file__).parents[2] / 'tools/debugmod/package.py'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload = b'mod-payload'
            (root / 'payload.bin').write_bytes(payload)
            manifest = {'format': 1, 'payload_size': len(payload),
                        'payload_sha256': hashlib.sha256(payload).hexdigest()}
            (root / 'manifest.json').write_text(json.dumps(manifest))
            patch, bundle = root / 'release.ttydpatch', root / 'release.zip'
            args = [sys.executable, str(tool), '--payload-dir', str(root),
                    '--output', str(patch), '--bundle', str(bundle)]
            subprocess.run(args, check=True, capture_output=True)
            with zipfile.ZipFile(patch) as archive:
                self.assertEqual(set(archive.namelist()), {'payload.bin', 'manifest.json'})
                self.assertEqual(archive.read('payload.bin'), payload)
            with zipfile.ZipFile(bundle) as archive:
                self.assertEqual(set(archive.namelist()), {'apply.py', 'TTYD-Essentials.ttydpatch', 'README.txt'})
                self.assertEqual(archive.read('TTYD-Essentials.ttydpatch'), patch.read_bytes())
            self.assertNotEqual(subprocess.run(args, capture_output=True).returncode, 0)
            with zipfile.ZipFile(bundle) as archive:
                self.assertEqual(patch.read_bytes(), archive.read('TTYD-Essentials.ttydpatch'))


if __name__ == '__main__':
    unittest.main()
