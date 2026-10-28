"""Keep the named mail-event flags tied to the game's scripts."""
import os
import re
import unittest
from pathlib import Path


class MailFlagTest(unittest.TestCase):
    def test_flag_to_mail_events(self):
        root = Path(__file__).parents[2]
        upstream = os.environ.get('TTYD_UPSTREAM')
        if not upstream:
            self.skipTest('Set TTYD_UPSTREAM to check the original event scripts')
        events = (Path(upstream) / 'src/event/evt_sub.c').read_text()
        mod = (root / 'mods/debug_menu.c').read_text()
        names = re.search(r'debug_mail_flags\[\]\s*=\s*\{(.*?)\};', mod, re.S).group(1)
        self.assertEqual(len(re.findall(r'"[^"]+"', names)), 16)
        for flag in range(7, 23):
            mail = flag + 9 if flag <= 16 else flag + 10
            pattern = rf'SET_VALUE\(GSWF\({flag}\), 1\)(?:(?!EVT_END\(\)).)*?CALL\(evt_pouch_receive_mail, {mail}\)'
            self.assertRegex(events.replace('\n', ' '), pattern)
