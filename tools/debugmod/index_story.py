#!/usr/bin/env python3
"""Export the game's English story-event IDs and destinations."""
import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
ENTRY = re.compile(r'\{\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*(\d+)\s*,\s*"([^"]+)"\s*,\s*"[^"]*"\s*NAME_EN\("([^"]+)"\)\s*,\s*"([^"]+)"\s*,\s*(NULL|"[^"]*")')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("upstream", type=Path, help="LLCOOLT/ttyd source checkout")
    upstream = parser.parse_args().upstream.resolve(strict=True)
    source = (upstream / 'src/event.c').read_text()
    entries = ENTRY.findall(source)
    if not entries:
        raise ValueError('No story events found; check source formatting')
    lines = ['# Story event reference', '',
             'Generated from the US story tables in `src/event.c` by `python3 tools/debugmod/index_story.py /path/to/upstream`. IDs are the game\'s event sequence values; some values have multiple entries. The game\'s own demo initializer sometimes sets progress to the preceding event ID before loading a selected event. Changing the raw progress value alone does not initialize inventory, partners, other flags, or a destination.', '',
             '| ID | Event | Area | Entrance |', '| ---: | --- | --- | --- |']
    for value, key, name, area, entrance in entries:
        entrance = entrance.strip('"') if entrance != 'NULL' else ''
        lines.append(f'| {value} | {name.replace("|", " / ")} | `{area}` | `{entrance}` |')
    target = ROOT / 'docs/STORY_EVENTS.md'
    target.write_text('\n'.join(lines) + '\n')
    print(f'Indexed {len(entries)} story events in {target}')


if __name__ == '__main__':
    main()
