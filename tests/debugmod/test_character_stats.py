"""Exercise damage bonuses and partner HP overrides with fake battle state."""
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class CharacterStatsTest(unittest.TestCase):
    def test_damage_and_health(self):
        compiler = shutil.which('/Library/Developer/CommandLineTools/usr/bin/clang') or shutil.which('cc')
        if not compiler:
            self.skipTest('C compiler not available')
        source = (Path(__file__).parents[2] / 'mods/debug_menu.c').read_text()
        def function(name):
            return re.search(r'(?:static )?(?:s32|void) ' + name + r'\([^)]*\) \{.*?\n\}', source, re.S).group()
        harness = r'''
#include <assert.h>
typedef int s32; typedef unsigned u32;
#define SEQ_TITLE 1
#define SEQ_LOGO 0
#define SEQ_GAME 2
#define SEQ_BATTLE 4
#define ITEM_HP_PLUS_P 99
typedef int BattleUnitType;
typedef struct {int mAlliance,currentKind; unsigned mTokenFlags;} BattleUnit;
typedef struct {int unused;} BattleUnitPart;
typedef struct {int unused;} BattleWeapon;
typedef struct {int baseMaxHP, maximumHP, currentHP;} PouchPartyData;
typedef struct {PouchPartyData partyData[8];} PouchData;
static int debug_attack_bonus[8], debug_defense_bonus[8], debug_partner_hp_override[8];
static int original_damage=5, sequence=SEQ_GAME, hp_badges=2;
static PouchData pouch;
static s32 BattleCalculateDamage(BattleUnit*a,BattleUnit*t,BattleUnitPart*p,BattleWeapon*w,u32*r,u32 f) {(void)a;(void)t;(void)p;(void)w;(void)f;*r=42;return original_damage;}
static s32 BattleTransPartyId(BattleUnitType kind) {return kind==0xe0 ? 1 : 2;}
static int seqGetSeq(void) {return sequence;}
static PouchData *pouchGetPtr(void) {return &pouch;}
static int pouchEquipCheckBadge(int id) {assert(id==ITEM_HP_PLUS_P);return hp_badges;}
''' + '\n'.join(function(n) for n in ('debug_battle_actor','debug_damage_hook','debug_apply_partner_hp')) + r'''
int main(void) {
    BattleUnit mario={0,0xde,0}, partner={0,0xe0,0}, enemy={1,0xe0,0}; u32 result;
    debug_attack_bonus[0]=3; debug_defense_bonus[1]=2;
    assert(debug_damage_hook(&mario,&enemy,0,0,&result,0)==8 && result==42);
    assert(debug_damage_hook(&enemy,&partner,0,0,&result,0)==3);
    debug_defense_bonus[1]=20; partner.mTokenFlags=2;
    assert(debug_damage_hook(&enemy,&partner,0,0,&result,4)==0 && result==(4|0x1000|0x1e));
    original_damage=0; assert(debug_damage_hook(&mario,&enemy,0,0,&result,0)==0 && result==42);
    original_damage=-3; assert(debug_damage_hook(&mario,&enemy,0,0,&result,0)==-3);
    debug_partner_hp_override[1]=25; pouch.partyData[1].currentHP=50;
    debug_apply_partner_hp(); assert(pouch.partyData[1].baseMaxHP==25 && pouch.partyData[1].maximumHP==35 && pouch.partyData[1].currentHP==35);
    sequence=SEQ_TITLE; debug_apply_partner_hp();
    assert(!debug_partner_hp_override[1] && !debug_attack_bonus[0] && !debug_defense_bonus[1]);
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
