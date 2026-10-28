"""Exercise the mod's wall flag and free-camera helpers with fake game state."""
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class ExplorationTest(unittest.TestCase):
    def test_camera_and_wall_flag_lifecycle(self):
        compiler = shutil.which('/Library/Developer/CommandLineTools/usr/bin/clang') or shutil.which('cc')
        if not compiler:
            self.skipTest('C compiler not available')
        source = (Path(__file__).parents[2] / 'mods/debug_menu.c').read_text()
        def function(name):
            return re.search(r'(?:static )?void ' + name + r'\([^)]*\) \{.*?\n\}', source, re.S).group()
        harness = r'''
#include <assert.h>
#include <stddef.h>
#include <math.h>
typedef float f32; typedef int s32;
typedef struct { float x,y,z; } Vec;
typedef struct { unsigned flags; int currMotionId; } MarioWork;
typedef struct CameraEntry CameraEntry;
typedef void (*CameraCallback)(CameraEntry *);
struct CameraEntry { Vec cameraPos, cameraAt; CameraCallback callback; };
typedef struct { signed char stickX[4], stickY[4], substickX[4], substickY[4]; unsigned char triggerRight[4], triggerLeft[4]; } GlobalWork;
#define MARIO_MOTION_VIVIAN 28
#define CAMERA_3D 4
#define SEQ_GAME 2
static MarioWork player;
static GlobalWork global, *gp=&global;
static int debug_wallpass, debug_wall_owned, debug_freecam, sequence=SEQ_GAME, transition, callback_suppressed, debug_cam_speed=1;
static Vec debug_cam_pos, debug_cam_at;
static f32 debug_cam_yaw, debug_cam_pitch, debug_cam_distance;
static CameraEntry camera;
static void original_callback(CameraEntry *c) { (void)c; }
static MarioWork *marioGetPtr(void) { return &player; }
static CameraEntry *camGetPtr(int id) { assert(id == CAMERA_3D); return &camera; }
static int seqGetSeq(void) { return sequence; }
static int seqCheckSeq(void) { return transition; }
static void camMain(void) { callback_suppressed = camera.callback == NULL; }
''' + '\n'.join(function(n) for n in ('debug_wall_update', 'debug_freecam_start', 'debug_freecam_move', 'debug_camera_hook')) + r'''
int main(void) {
    debug_wallpass=1; debug_wall_update(); assert((player.flags & 0x400) && debug_wall_owned);
    debug_wallpass=0; player.currMotionId=MARIO_MOTION_VIVIAN; debug_wall_update(); assert(player.flags & 0x400);
    player.currMotionId=0; debug_wall_update(); assert(!(player.flags & 0x400) && !debug_wall_owned);
    player.flags=0x400; debug_wallpass=1; debug_wall_update(); debug_wallpass=0; debug_wall_update(); assert(player.flags & 0x400);
    camera.cameraPos=(Vec){0,0,0}; camera.cameraAt=(Vec){0,0,-100};
    debug_freecam_start(&camera);
    assert(fabsf(debug_cam_yaw)<0.001f && fabsf(debug_cam_pitch)<0.001f && fabsf(debug_cam_distance-100)<0.001f);
    global.stickY[0]=10; debug_freecam_move();
    assert(fabsf(debug_cam_pos.x)<0.001f && debug_cam_pos.z < -1.59f && debug_cam_pos.z > -1.61f);
    debug_cam_pos=(Vec){0,0,0}; debug_cam_yaw=1.5707963268f;
    debug_freecam_move(); assert(debug_cam_pos.x>1.59f && debug_cam_pos.x<1.61f && fabsf(debug_cam_pos.z)<0.001f);
    global.stickY[0]=0; global.stickX[0]=10; debug_cam_pos=(Vec){0,0,0};
    debug_freecam_move(); assert(debug_cam_pos.z>1.59f && debug_cam_pos.z<1.61f && fabsf(debug_cam_pos.x)<0.001f);
    global.stickX[0]=0; global.substickX[0]=10; debug_cam_yaw=0; global.triggerRight[0]=0;
    debug_freecam_move(); {float yaw_without_trigger=debug_cam_yaw;
        debug_cam_yaw=0; global.triggerRight[0]=200; debug_freecam_move();
        assert(fabsf(debug_cam_yaw-yaw_without_trigger)<0.00001f);
        assert(fabsf(sqrtf((debug_cam_at.x-debug_cam_pos.x)*(debug_cam_at.x-debug_cam_pos.x) +
                           (debug_cam_at.y-debug_cam_pos.y)*(debug_cam_at.y-debug_cam_pos.y) +
                           (debug_cam_at.z-debug_cam_pos.z)*(debug_cam_at.z-debug_cam_pos.z))-100)<0.01f);
    }
    debug_cam_speed=5; debug_cam_yaw=0; global.substickX[0]=0; global.stickX[0]=10; debug_cam_pos=(Vec){0,0,0};
    debug_freecam_move(); assert(debug_cam_pos.x>7.99f && debug_cam_pos.x<8.01f);
    camera.callback=original_callback; debug_freecam=1; debug_camera_hook();
    assert(callback_suppressed && camera.callback==original_callback && camera.cameraPos.x==debug_cam_pos.x);
    debug_freecam=0; debug_camera_hook(); assert(!callback_suppressed && camera.callback==original_callback);
    debug_freecam=1; transition=1; debug_camera_hook(); assert(!callback_suppressed);
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
            subprocess.run(args + [str(cfile), '-o', str(exe), '-lm'], check=True)
            subprocess.run([str(exe)], check=True)
