#!/usr/bin/env python3
"""Create a small redistributable patch and a standalone installer bundle."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--payload-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True, help='new .ttydpatch path')
    parser.add_argument('--bundle', type=Path, help='new installer ZIP path')
    args = parser.parse_args()
    payload = (args.payload_dir / 'payload.bin').read_bytes()
    manifest_bytes = (args.payload_dir / 'manifest.json').read_bytes()
    manifest = json.loads(manifest_bytes)
    if manifest.get('format') != 1 or not 0 < len(payload) <= 0x7400 or len(payload) != manifest.get('payload_size') or hashlib.sha256(payload).hexdigest() != manifest.get('payload_sha256'):
        raise ValueError('Invalid payload or manifest')
    if args.output.exists() or (args.bundle and args.bundle.exists()):
        raise ValueError('Output already exists; choose a new path')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('payload.bin', payload)
        archive.writestr('manifest.json', manifest_bytes)
    if args.bundle:
        args.bundle.parent.mkdir(parents=True, exist_ok=True)
        instructions = ('TTYD Essentials\n\nRequires Python 3 and an original US G8ME01 revision 0 ISO.\n'
                        'Extract the entire archive, then run:\n\n'
                        'python3 apply.py /path/to/original.iso /path/to/new-output.iso --patch TTYD-Essentials.ttydpatch\n\n'
                        'The output must not exist. The original image is not modified.\n')
        with zipfile.ZipFile(args.bundle, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr('apply.py', (Path(__file__).parent / 'patch.py').read_bytes())
            archive.write(args.output, 'TTYD-Essentials.ttydpatch')
            archive.writestr('README.txt', instructions)
    print(f'Created {args.output}')
    if args.bundle:
        print(f'Created {args.bundle}')


if __name__ == '__main__':
    main()
