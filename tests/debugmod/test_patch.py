import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('debug_patch', Path(__file__).parents[2] / 'tools/debugmod/patch.py')
patch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(patch)

class BranchTest(unittest.TestCase):
    def test_forward_and_backward_link_branches(self):
        self.assertEqual(patch.branch(0x80000000, 0x80000004), 0x48000005)
        self.assertEqual(patch.branch(0x80000004, 0x80000000), 0x4bfffffd)

    def test_out_of_range_or_unaligned(self):
        for target in (0x82000000, 0x7dfffffc, 0x80000002):
            with self.assertRaises(ValueError):
                patch.branch(0x80000000, target)

if __name__ == '__main__':
    unittest.main()

class MapOrderTest(unittest.TestCase):
    def test_named_rooms_match_game_map_order(self):
        import re
        root = Path(__file__).parents[2]
        import os
        upstream = os.environ.get('TTYD_UPSTREAM')
        game = (Path(upstream) / 'src/data/mapdata.c').read_text() if upstream else None
        menu = (root / 'mods/debug_menu.c').read_text()
        expected = {
            'gor': ['gor_00', 'gor_01', 'gor_02', 'gor_03', 'gor_04', 'gor_10', 'gor_11', 'gor_12'],
            'tik': ['tik_00', 'tik_01', 'tik_02', 'tik_03', 'tik_04', 'tik_05', 'tik_06', 'tik_07', 'tik_08', 'tik_11', 'tik_12', 'tik_13', 'tik_15', 'tik_16', 'tik_17', 'tik_18', 'tik_19', 'tik_20', 'tik_21'],
        }
        for area, names in expected.items():
            if game is not None:
                definition = re.search(r'AreaData area_' + area + r'\s*=\s*\{(.*?)\};', game, re.S).group(1)
                self.assertEqual(re.findall(r'&(' + area + r'_\w+)', definition), names)
            descriptions = re.search(r'debug_' + area + r'_rooms\[\]\s*=\s*\{(.*?)\};', menu, re.S).group(1)
            self.assertEqual(len(re.findall(r'"[^"]*"', descriptions)), len(names))
