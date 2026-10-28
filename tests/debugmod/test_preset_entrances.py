"""Exercise story preset guards/order and live entrance lookup."""
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class PresetEntrancesTest(unittest.TestCase):
    def test_helpers(self):
        compiler = shutil.which('/Library/Developer/CommandLineTools/usr/bin/clang') or shutil.which('cc')
        if not compiler:
            self.skipTest('C compiler not available')
        source = (Path(__file__).parents[2] / 'mods/debug_menu.c').read_text()
        def function(name):
            return re.search(r'static (?:s32|BOOL|const char\*) ' + name + r'\([^\n]*\) \{.*?\n\}', source, re.S).group()
        harness = r'''
#include <assert.h>
#include <stddef.h>
#include <string.h>
typedef int s32; typedef int BOOL; typedef int PartyId;
#define TRUE 1
#define FALSE 0
#define SEQ_MAP_CHANGE 3
typedef struct {int id, motionType; int partners[2]; const char *mapName,*beroName; void (*initEvent)(void);} EventData;
typedef struct {EventData *data; int count;} EventStage;
typedef struct {int prevPartyMemberId[2];} MarioWork;
typedef struct {int systemLevelFlags; char currentMapName[16];} GlobalWork;
typedef struct {const char *hitName;} BeroEntry;
static int debug_freecam=1, debug_wallpass=1, debug_stat_locks=7, available=1, busy, resets, swvalue=-1, init_count, lastseq, count=2;
static int calls[8], call_count, entry_count;
static MarioWork player={{1,2}};
static GlobalWork global={0,"gor_00"}, *gp=&global;
static BeroEntry a={"door_a"}, b={"pipe_b"}; static BeroEntry *doors[2]={&a,&b};
static void init1(void) { calls[call_count++]=1; init_count++; }
static void init2(void) { calls[call_count++]=2; init_count++; }
static EventData events[] = {{0,0,{0,0},"gor_00","door_a",init1},{4,1,{1,2},"gor_00","pipe_b",init2},{5,0,{0,0},"gor_00",0,0}};
static EventStage stage={events,3};
static EventData *debug_story_event(int id,int mode) { if(id!=4)return 0; return mode==2 ? &events[0] : &events[1]; }
static int mapDataPtr(const char *s) { return s && available; }
static int debug_destination_available(const char *s) { return s && available; }
static int marioKeyOffChk(void) { return busy; }
static void debug_wall_update(void) {}
static void marioPartyKill(void) { calls[call_count++]=3; }
static void swInit(void) { resets++; calls[call_count++]=4; }
static void swByteSet(int id,int value) { assert(id==0); swvalue=value; }
static int eventStgNum(void) { return 1; }
static EventStage *eventStgDtPtr(int id) { assert(id==0); return &stage; }
static void marioChgShipMotion(void) { calls[call_count++]=5; }
static void marioChgStayMotion(void) { calls[call_count++]=6; }
static MarioWork *marioGetPtr(void) { return &player; }
static int marioPartyEntry(int id) { assert(id==1 || id==2); entry_count++; return 0; }
static void pouchReviseMarioParam(void) {}
static void pouchRevisePartyParam(void) {}
static void statusWinForceUpdate(void) {}
static void seqSetSeq(int seq,const char *map,const char *entrance) { assert(seq==3 && !strcmp(map,"gor_00") && !strcmp(entrance,"pipe_b")); lastseq=seq; }
static int bero_get_BeroNUM(void) { return count; }
static BeroEntry **bero_get_ptr(void) { return doors; }
''' + '\n'.join(function(n) for n in ('debug_clamp','debug_apply_preset','debug_entrance_count','debug_entrance_current')) + r'''
int main(void) {
    assert(debug_entrance_count("gor_00")==2 && debug_entrance_count("tik_00")==0);
    assert(!strcmp(debug_entrance_current("gor_00",1),"pipe_b"));
    assert(debug_entrance_current("gor_00",2)==0 && debug_entrance_current("tik_00",0)==0);
    count=30; assert(debug_entrance_count("gor_00")==16);
    available=0; assert(!debug_apply_preset(4) && resets==0);
    available=1; busy=1; assert(!debug_apply_preset(4) && resets==0);
    busy=0; assert(debug_apply_preset(4));
    assert(!debug_freecam && !debug_wallpass && !debug_stat_locks && resets==1 && swvalue==0);
    assert(call_count==5 && calls[0]==3 && calls[1]==4 && calls[2]==1 && calls[3]==2 && calls[4]==5);
    assert(init_count==2 && entry_count==2 && !player.prevPartyMemberId[0] && !player.prevPartyMemberId[1] && lastseq==3);
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
