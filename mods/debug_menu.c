/* G8ME01 in-game state inspector, built as an address-stable injected payload. */
#include "mario/mariost.h"
#include "mario/mario.h"
#include "mario/mario_party.h"
#include "battle/battle_unit.h"
#include "battle/battle_database_common.h"
#include "driver/camdrv.h"
#include "driver/dispdrv.h"
#include "driver/seqdrv.h"
#include "driver/swdrv.h"
#include "manager/fontmgr.h"
#include "system.h"
#include "event.h"
#include "manager/evtmgr.h"
#include "evt/evt_bero.h"
#include "data/item_data.h"
#include "driver/msgdrv.h"
#include <string.h>
#include "data/mapdata.h"
#include <dolphin/pad.h>
#include <dolphin/os.h>
#include <dolphin/dvd.h>
#include <stdio.h>
#include <math.h>

extern WorldData world_data;
extern void effMain(void);
/* The bundled GameCube math header omits this declaration. Without it,
 * MWCC assumes an integer return and corrupts the camera angles. */
extern double atan2(double y, double x);
extern void partyKill(s32 slot);
extern void marioChgStayMotion(void);
extern void marioChgShipMotion(void);
extern EvtWord mobj_save_blk_sysevt[];
extern void statusWinForceUpdate(void);
extern s32 BattleTransPartyId(BattleUnitType kind);
extern s32 BattleCalculateDamage(BattleUnit* attacker, BattleUnit* target, BattleUnitPart* part,
                                 BattleWeapon* weapon, u32* result, u32 flags);
extern ItemData itemDataTable[];
static WorldData* debug_world(void) { return &world_data; }
static int debug_area_count(void) {
    int n = 0;
    while (n < 64 && world_data.areas[n]) ++n;
    return n;
}
static int debug_room_count(const AreaData* area) {
    int n = 0;
    while (n < 256 && area->maps[n]) ++n;
    return n;
}
extern void FontDrawScale(f32 scale);
extern void FontDrawEdge(void);
extern void FontDrawString(f32 x, f32 y, const char* text);

/* Follows world_data.areas in src/data/mapdata.c. Where no official English
 * name is established, these are plain descriptions of the source labels. */
static const char* const debug_area_names[] = {
    "TEST MAPS", "BATTLE STAGE", "BACKDROPS", "MARIO'S HOUSE",
    "ROGUEPORT", "ROGUEPORT UNDERGROUND", "HOOKTAIL CASTLE", "PETAL MEADOWS",
    "PETALBURG", "BOGGLY WOODS", "GREAT TREE", "GLITZ PIT",
    "TWILIGHT TOWN", "TWILIGHT TRAIL", "CREEPY STEEPLE", "KEELHAUL KEY",
    "PIRATE GROTTO", "POSHLEY HEIGHTS", "EXCESS EXPRESS", "TRAIN PLATFORM",
    "STATION", "FAHR OUTPOST", "MOON", "X-NAUT BASE",
    "PALACE OF SHADOW", "BOWSER STAGES", "PIT OF 100 TRIALS", "PIANTA PARLOR",
    "QUIZ ROOM", "SYSTEM ROOMS", "OPENING DEMO", "RECAP", "ENDING"
};

/* Room descriptions checked against the community room ID list; ordering
 * comes from each area's maps array in src/data/mapdata.c. */
static const char* const debug_gor_rooms[] = {
    "HARBOR", "MAIN SQUARE", "EAST SIDE", "WEST SIDE", "STATION",
    "ARRIVAL CUTSCENE", "OUTSIDE AT DUSK", "OUTSIDE AT DAWN"
};
static const char* const debug_tik_rooms[] = {
    "SHOP AREA", "EAST ENTRANCE", "PIPE TO PETAL MEADOWS", "PIPE TO BOGGLY WOODS",
    "STAIRCASE", "THOUSAND-YEAR DOOR", "PIT ENTRANCE", "WEST ENTRANCE",
    "PIPE TO TWILIGHT TOWN", "CHET RIPPO'S HOUSE", "MERLEE'S HOUSE", "STORAGE ROOM",
    "CORRIDOR", "UNDERGROUND CORRIDOR 1", "UNDERGROUND CORRIDOR 2",
    "UNDERGROUND CORRIDOR 3", "BLACK CHEST ROOM", "HIDDEN CHAMBER", "SPIKE TRAP ROOM"
};
static const char* debug_room_name(s32 area, s32 room) {
    if (area == 4 && room < 8) return debug_gor_rooms[room];
    if (area == 5 && room < 19) return debug_tik_rooms[room];
    return NULL;
}

/* Each flag marks execution of a mail event in evt_sub.c. These are not
 * the mail inventory bits: changing one does not deliver or delete mail. */
static const char* const debug_mail_flags[] = {
    "FRANKLY MAIL EVENT", "KOOPLEY MAIL EVENT", "KOOPIE KOO MAIL EVENT",
    "PETUNI MAIL EVENT", "BOO MAIL EVENT", "PA-PATCH MAIL EVENT",
    "KING K MAIL EVENT", "ZIP TOAD MAIL EVENT", "RAWK HAWK MAIL EVENT",
    "GHOST T MAIL EVENT", "NEWSLETTER PREMIERE EVENT", "NEWSLETTER 2 EVENT",
    "NEWSLETTER 3 EVENT", "NEWSLETTER 4 EVENT", "NEWSLETTER 5 EVENT",
    "NEWSLETTER 6 EVENT"
};

static const char* debug_flag_name(s32 flag) {
    /* Score-record conditions in rels/yuu/src/event/evt_yuuranking.c. */
    if (flag >= 7 && flag <= 22) return debug_mail_flags[flag - 7];
    switch (flag) {
        case 0: return "SHOP TUTORIAL SEEN";
        case 37: return "FIRST EMAIL RECEIVED";
        case 38: return "EMAIL READ";
        case 233: return "SAVE BLOCK TUTORIAL SEEN";
        case 234: return "HEALING BLOCK TUTORIAL SEEN";
        case 235: return "ITEM TUTORIAL SEEN";
        case 1213: return "GUS FIGHT FLAG";
        case 1498: return "HOOKTAIL FIGHT FLAG";
        case 2226: return "ATOMIC BOO FIGHT FLAG";
        case 2388: return "GLITZ PIT MATCH RESERVED";
        case 2443: return "PREVIOUS GLITZ MATCH WON";
        case 1240: return "ARCADE TYPE 0 TOP SCORE";
        case 1241: return "ARCADE TYPE 3 TOP SCORE";
        case 1242: return "ARCADE TOP SCORE";
        case 1243: return "ARCADE SCORE RECORD";
        default: return "UNKNOWN - RAW GAME FLAG";
    }
}

/* Check the actual inserted disc before the game starts its map transition.
 * Map dmo_00 deliberately loads gor_01 geometry (seq_mapchange.c). */
static BOOL debug_destination_available(const char* map) {
    char path[64];
    const char* geometry = !strcmp(map, "dmo_00") ? "gor_01" : map;
    sprintf(path, "/rel/%c%c%c.rel", map[0], map[1], map[2]);
    if (DVDConvertPathToEntrynum(path) < 0) return FALSE;
    sprintf(path, "/m/%s/d", geometry);
    return DVDConvertPathToEntrynum(path) >= 0;
}

static const s32 debug_known_flags[] = {
    0, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
    37, 38, 233, 234, 235, 1213, 1240, 1241, 1242, 1243,
    1498, 2226, 2388, 2443
};
static s32 debug_next_known_flag(s32 flag) {
    s32 i;
    for (i = 0; i < (s32)(sizeof(debug_known_flags) / sizeof(debug_known_flags[0])); ++i)
        if (debug_known_flags[i] > flag) return debug_known_flags[i];
    return debug_known_flags[0];
}

/* Modes: 0 = first exact event, 1 = next numeric ID, 2 = previous
 * entry in table order (the game's demo initializer uses that value). */
static EventData* debug_story_event(s32 value, BOOL next) {
    EventData* best = NULL;
    s32 stage_id, i;
    for (stage_id = 0; stage_id < eventStgNum(); ++stage_id) {
        EventStage* stage = eventStgDtPtr(stage_id);
        for (i = 0; i < stage->count; ++i) {
            EventData* event = &stage->data[i];
            if (next == 2) {
                if (event->id == value) return best;
                best = event;
                continue;
            }
            if ((!next && event->id == value) ||
                (next && event->id > value && (!best || event->id < best->id))) {
                best = event;
                if (!next) return best;
            }
        }
    }
    return next == 2 ? NULL : best;
}

static const char* const debug_characters[] = {"MARIO", "PEACH", "BOWSER"};
static const char* const debug_partners[] = {
    "GOOMBELLA", "KOOPS", "BOBBERY", "YOSHI", "FLURRIE", "VIVIAN", "MS MOWZ"
};
static u32 debug_stat_locks;
static s32 debug_locked_values[7];
static s32 debug_page;
static s32 debug_freecam;
static s32 debug_cam_speed = 1;
static s32 debug_preset_id;
static s32 debug_preset_confirm;
static s32 debug_preset_error;
static s32 debug_entrance = -1;
static char debug_entrance_name[64];
static s32 debug_item_kind;
static s32 debug_item_id = 0x80;
static s32 debug_item_status;
static s32 debug_stat_actor;
static s32 debug_attack_bonus[8];
static s32 debug_defense_bonus[8];
static s32 debug_partner_hp_override[8];
static s32 debug_wallpass;
static s32 debug_wall_owned;
static Vec debug_cam_pos;
static Vec debug_cam_at;
static f32 debug_cam_yaw;
static f32 debug_cam_pitch;
static f32 debug_cam_distance;
static s32 debug_save_event;
static s32 debug_save_error;
static s32 debug_character;
static const char* const debug_partner_levels[] = {"NORMAL", "SUPER", "ULTRA"};

/* Dismiss only the active partner, preserving any separate story follower. */
static void debug_dismiss_partner(void) {
    MarioWork* mario = marioGetPtr();
    s32 slot = marioGetPartyId();
    if (slot < 0) return;
    partyKill(slot);
    if (mario->currPartySlotId[0] == slot) mario->currPartySlotId[0] = -1;
    if (mario->currPartySlotId[1] == slot) mario->currPartySlotId[1] = -1;
}

/* Match the game's upgrade routine, including recalculated maximum HP. */
static void debug_advance_partner(PartyId id) {
    PouchPartyData* partner = &pouchGetPtr()->partyData[id];
    s32 level;
    if (!partyChkJoin(id)) {
        partyJoin(id);
        level = 0;
    } else if (partner->techLevel < 2) {
        level = partner->techLevel + 1;
        if (level < 0) level = 0;
    } else {
        if (marioGetParty() == id) debug_dismiss_partner();
        partyLeft(id);
        return;
    }
    partner->HPLevel = partner->attackLevel = partner->techLevel = level;
    pouchRevisePartyParam();
    partner->currentHP = partner->maximumHP;
}

static s32 debug_open;
static s32 debug_consume;
static s32 debug_row;
static s32 debug_byte = 1;
static s32 debug_flag;
static s32 debug_area = 4; /* gor / Rogueport */
static s32 debug_room;
static u32 debug_previous;

static s32 debug_wrap(s32 value, s32 count) {
    if (value < 0) return count - 1;
    if (value >= count) return 0;
    return value;
}

static s32 debug_clamp(s32 value, s32 low, s32 high) {
    if (value < low) return low;
    if (value > high) return high;
    return value;
}

static s32 debug_read_stat(PouchData* pouch, s32 row) {
    switch (row) {
        case 0: return pouch->currentHP;
        case 1: return pouch->baseMaxHP;
        case 2: return pouch->currentFP;
        case 3: return pouch->baseMaxFP;
        case 4: return pouch->maximumBP;
        case 5: return pouch->coins;
        case 6: return pouch->mStarPieceCount;
        default: return 0;
    }
}

static void debug_change_stat(s32 row, s32 delta) {
    PouchData* pouch = pouchGetPtr();
    s32 spent;
    switch (row) {
        case 0: pouch->currentHP = debug_clamp(pouch->currentHP + delta, 1, pouch->maximumHP); break;
        case 1: pouch->baseMaxHP = debug_clamp(pouch->baseMaxHP + delta, 1, 99); pouchReviseMarioParam(); break;
        case 2: pouch->currentFP = debug_clamp(pouch->currentFP + delta, 0, pouch->maximumFP); break;
        case 3: pouch->baseMaxFP = debug_clamp(pouch->baseMaxFP + delta, 0, 99); pouchReviseMarioParam(); break;
        case 4:
            spent = pouch->maximumBP - pouch->availableBP;
            if (spent < 0) spent = 0;
            if (spent <= 99) {
                pouch->maximumBP = debug_clamp(pouch->maximumBP + delta, spent, 99);
                pouchReviseMarioParam();
            }
            break;
        case 5: pouchSetCoin(debug_clamp((s32)pouch->coins + delta, 0, 999)); break;
        case 6: pouch->mStarPieceCount = debug_clamp((s32)pouch->mStarPieceCount + delta, 0, 999); break;
        default: return;
    }
    if (debug_stat_locks & (1u << row)) debug_locked_values[row] = debug_read_stat(pouch, row);
    statusWinForceUpdate();
}

/* Restore enabled locks once per frame; maximum values are recalculated using
 * the game's badge rules before restoring current HP and FP. */
static void debug_apply_stat_locks(void) {
    PouchData* pouch;
    s32 seq = seqGetSeq();
    s32 spent, desired;
    BOOL recalc = FALSE;
    BOOL changed = FALSE;
    if (seq == SEQ_TITLE || seq == SEQ_LOGO) { debug_stat_locks = 0; return; }
    if (!debug_stat_locks || (seq != SEQ_GAME && seq != SEQ_BATTLE)) return;
    pouch = pouchGetPtr();
    if ((debug_stat_locks & 2) && pouch->baseMaxHP != debug_locked_values[1]) {
        pouch->baseMaxHP = debug_locked_values[1]; recalc = TRUE;
    }
    if ((debug_stat_locks & 8) && pouch->baseMaxFP != debug_locked_values[3]) {
        pouch->baseMaxFP = debug_locked_values[3]; recalc = TRUE;
    }
    if (debug_stat_locks & 16) {
        spent = pouch->maximumBP - pouch->availableBP;
        if (spent < 0) spent = 0;
        desired = debug_locked_values[4];
        if (desired < spent) desired = spent;
        if (pouch->maximumBP != desired) { pouch->maximumBP = desired; recalc = TRUE; }
    }
    if (recalc) { pouchReviseMarioParam(); changed = TRUE; }
    if (debug_stat_locks & 1) {
        desired = debug_clamp(debug_locked_values[0], 1, pouch->maximumHP);
        if (pouch->currentHP != desired) { pouch->currentHP = desired; changed = TRUE; }
    }
    if (debug_stat_locks & 4) {
        desired = debug_clamp(debug_locked_values[2], 0, pouch->maximumFP);
        if (pouch->currentFP != desired) { pouch->currentFP = desired; changed = TRUE; }
    }
    if ((debug_stat_locks & 32) && pouch->coins != debug_locked_values[5]) {
        pouchSetCoin(debug_locked_values[5]); changed = TRUE;
    }
    if ((debug_stat_locks & 64) && pouch->mStarPieceCount != debug_locked_values[6]) {
        pouch->mStarPieceCount = debug_locked_values[6]; changed = TRUE;
    }
    if (changed) statusWinForceUpdate();
}

/* Start the same event as a save block, with room for its child events. */
static BOOL debug_start_save(void) {
    EventWork* work = evtGetWork();
    EventEntry* event;
    s32 free_count = 0;
    s32 i;
    if (debug_save_event || gp->systemLevelFlags || !work || !work->entries) return FALSE;
    for (i = 0; i < work->count; ++i)
        if (!(work->entries[i].flags & EVENT_ACTIVE)) ++free_count;
    if (free_count < 4) return FALSE;
    marioStSystemLevel(1);
    event = evtEntryType(mobj_save_blk_sysevt, 0x1e, 0, 0x1a);
    debug_save_event = event->eventId;
    return TRUE;
}

/* The game's 0x400 movement flag bypasses horizontal wall checks; ground
 * detection remains in the normal player update. Preserve pre-existing use. */
static void debug_wall_update(void) {
    MarioWork* mario = marioGetPtr();
    if (debug_wallpass) {
        if (!(mario->flags & 0x400)) { mario->flags |= 0x400; debug_wall_owned = 1; }
    } else if (debug_wall_owned && mario->currMotionId != MARIO_MOTION_VIVIAN) {
        mario->flags &= ~0x400u;
        debug_wall_owned = 0;
    }
}

/* Retain a fixed look distance and angular aim, so translation does not
 * alter sensitivity. Yaw zero faces world -Z; movement follows camera yaw. */
static void debug_freecam_start(CameraEntry* camera) {
    f32 dx, dy, dz, horizontal;
    debug_cam_pos = camera->cameraPos;
    debug_cam_at = camera->cameraAt;
    dx = debug_cam_at.x - debug_cam_pos.x;
    dy = debug_cam_at.y - debug_cam_pos.y;
    dz = debug_cam_at.z - debug_cam_pos.z;
    horizontal = (f32)sqrt(dx * dx + dz * dz);
    debug_cam_distance = (f32)sqrt(horizontal * horizontal + dy * dy);
    if (debug_cam_distance < 1.0f) debug_cam_distance = 100.0f;
    debug_cam_yaw = (f32)atan2(dx, -dz);
    debug_cam_pitch = (f32)atan2(dy, horizontal);
    if (debug_cam_pitch > 1.4f) debug_cam_pitch = 1.4f;
    if (debug_cam_pitch < -1.4f) debug_cam_pitch = -1.4f;
}

static void debug_freecam_move(void) {
    f32 forward, right, up, sin_yaw, cos_yaw, cos_pitch;
    debug_cam_yaw += gp->substickX[0] * (0.0006f * debug_cam_speed);
    debug_cam_pitch += gp->substickY[0] * (0.0006f * debug_cam_speed);
    if (debug_cam_pitch > 1.4f) debug_cam_pitch = 1.4f;
    if (debug_cam_pitch < -1.4f) debug_cam_pitch = -1.4f;
    sin_yaw = (f32)sin(debug_cam_yaw);
    cos_yaw = (f32)cos(debug_cam_yaw);
    cos_pitch = (f32)cos(debug_cam_pitch);
    right = gp->stickX[0] * (0.16f * debug_cam_speed);
    forward = gp->stickY[0] * (0.16f * debug_cam_speed);
    up = ((s32)gp->triggerRight[0] - (s32)gp->triggerLeft[0]) * (0.05f * debug_cam_speed);
    debug_cam_pos.x += right * cos_yaw + forward * sin_yaw;
    debug_cam_pos.y += up;
    debug_cam_pos.z += right * sin_yaw - forward * cos_yaw;
    debug_cam_at.x = debug_cam_pos.x + debug_cam_distance * cos_pitch * sin_yaw;
    debug_cam_at.y = debug_cam_pos.y + debug_cam_distance * (f32)sin(debug_cam_pitch);
    debug_cam_at.z = debug_cam_pos.z - debug_cam_distance * cos_pitch * cos_yaw;
}

/* Rebuild the view matrix from our camera without permanently replacing the
 * game's camera callback. It resumes normally when free-cam is disabled. */
void debug_camera_hook(void) {
    CameraEntry* camera;
    CameraCallback callback;
    if (!debug_freecam || seqGetSeq() != SEQ_GAME || seqCheckSeq()) {
        camMain();
        return;
    }
    camera = camGetPtr(CAMERA_3D);
    callback = camera->callback;
    camera->cameraPos = debug_cam_pos;
    camera->cameraAt = debug_cam_at;
    camera->callback = NULL;
    camMain();
    camera->callback = callback;
}

/* Replicate the game's E3 event preparation. It resets saved flags and
 * pouch contents; this action is only called after explicit confirmation. */
static BOOL debug_apply_preset(s32 id) {
    EventData* target = debug_story_event(id, FALSE);
    EventData* previous;
    MarioWork* mario;
    s32 stage_id, i;
    if (!target || !target->mapName || !mapDataPtr(target->mapName) ||
        !debug_destination_available(target->mapName) || gp->systemLevelFlags || marioKeyOffChk()) return FALSE;
    previous = debug_story_event(id, 2);
    debug_freecam = 0;
    debug_wallpass = 0;
    debug_wall_update();
    debug_stat_locks = 0;
    marioPartyKill();
    swInit();
    swByteSet(0, previous ? previous->id : 0);
    for (stage_id = 0; stage_id < eventStgNum(); ++stage_id) {
        EventStage* stage = eventStgDtPtr(stage_id);
        for (i = 0; i < stage->count; ++i) {
            EventData* event = &stage->data[i];
            if (event->initEvent) event->initEvent();
            if (event == target) goto initialized;
        }
    }
initialized:
    if (target->motionType == 1) marioChgShipMotion(); else marioChgStayMotion();
    mario = marioGetPtr();
    mario->prevPartyMemberId[0] = mario->prevPartyMemberId[1] = 0;
    if (target->partners[0]) marioPartyEntry((PartyId)target->partners[0]);
    if (target->partners[1]) marioPartyEntry((PartyId)target->partners[1]);
    pouchReviseMarioParam();
    pouchRevisePartyParam();
    statusWinForceUpdate();
    seqSetSeq(SEQ_MAP_CHANGE, target->mapName, target->beroName);
    return TRUE;
}

static s32 debug_entrance_count(const char* target) {
    s32 count;
    if (strcmp(target, gp->currentMapName)) return 0;
    count = bero_get_BeroNUM();
    return debug_clamp(count, 0, 16);
}

static const char* debug_entrance_current(const char* target, s32 index) {
    BeroEntry** entries;
    if (index < 0 || index >= debug_entrance_count(target)) return NULL;
    entries = bero_get_ptr();
    if (!entries || !entries[index]) return NULL;
    return entries[index]->hitName;
}

/* Flat modifiers apply only to ordinary positive HP damage calculated by
 * BattleCheckDamage. Healing, immunity, FP and scripted damage are unchanged. */
static s32 debug_battle_actor(BattleUnit* unit) {
    s32 id;
    if (!unit || unit->mAlliance != 0) return -1;
    if (unit->currentKind == 0xde) return 0;
    if (unit->currentKind < 0xe0 || unit->currentKind > 0xe6) return -1;
    id = BattleTransPartyId(unit->currentKind);
    return id >= 1 && id <= 7 ? id : -1;
}

s32 debug_damage_hook(BattleUnit* attacker, BattleUnit* target, BattleUnitPart* part,
                      BattleWeapon* weapon, u32* result, u32 flags) {
    s32 damage = BattleCalculateDamage(attacker, target, part, weapon, result, flags);
    s32 source, destination;
    if (damage <= 0) return damage;
    source = debug_battle_actor(attacker);
    destination = debug_battle_actor(target);
    if (source >= 0) damage += debug_attack_bonus[source];
    if (destination >= 0) damage -= debug_defense_bonus[destination];
    if (damage <= 0) {
        if (target && (target->mTokenFlags & 2)) flags |= 0x1000;
        *result = flags | 0x1e;
        return 0;
    }
    return damage;
}

/* Preserve custom partner maxima across the game's normal parameter refreshes. */
static void debug_apply_partner_hp(void) {
    s32 i, bonus;
    PouchData* pouch;
    s32 seq = seqGetSeq();
    if (seq == SEQ_TITLE || seq == SEQ_LOGO) {
        for (i = 0; i < 8; ++i) {
            debug_partner_hp_override[i] = 0;
            debug_attack_bonus[i] = debug_defense_bonus[i] = 0;
        }
        return;
    }
    if (seq != SEQ_GAME && seq != SEQ_BATTLE) return;
    pouch = pouchGetPtr();
    bonus = pouchEquipCheckBadge(ITEM_HP_PLUS_P) * 5;
    for (i = 1; i < 8; ++i) {
        PouchPartyData* partner = &pouch->partyData[i];
        if (debug_partner_hp_override[i]) {
            partner->baseMaxHP = debug_partner_hp_override[i];
            partner->maximumHP = partner->baseMaxHP + bonus;
            if (partner->currentHP > partner->maximumHP) partner->currentHP = partner->maximumHP;
        }
    }
}

static void debug_menu_input(void) {
    const u32 held = gp->button[0];
    const u32 pressed = held & ~debug_previous;
    const u32 chord = PAD_TRIGGER_L | PAD_TRIGGER_R | PAD_TRIGGER_Z;
    s32 direction;
    s32 step;
    WorldData* world;
    AreaData* area;
    s32 area_count;
    s32 room_count;
    debug_previous = held;
    if (debug_save_event) {
        if (evtCheckID(debug_save_event)) return;
        debug_save_event = 0;
        marioStSystemLevel(0);
    }
    if (seqGetSeq() != SEQ_GAME || seqCheckSeq()) {
        debug_freecam = 0;
        debug_wallpass = 0;
        debug_wall_update();
        debug_open = 0;
        debug_consume = 0;
        return;
    }
    debug_wall_update();
    if ((held & chord) == chord && (pressed & PAD_BUTTON_START)) {
        debug_open = !debug_open;
        debug_consume = 1;
    }
    if (debug_open) {
        /* L changes pages. The full opening/closing chord is never a page turn. */
        if ((pressed & PAD_TRIGGER_L) && (held & chord) != chord) {
            debug_page = (debug_page + 1) % 8;
            debug_save_error = 0;
            debug_preset_confirm = debug_preset_error = 0;
            debug_preset_id = swByteGet(0);
            debug_row = 0;
            debug_character = marioGetPtr()->characterId;
            if (debug_character < 0 || debug_character > 2) debug_character = 0;
        }
        if (debug_page == 7) {
            PouchData* pouch = pouchGetPtr();
            if (pressed & PAD_BUTTON_UP) debug_row = debug_wrap(debug_row - 1, 5);
            if (pressed & PAD_BUTTON_DOWN) debug_row = debug_wrap(debug_row + 1, 5);
            direction = (pressed & PAD_BUTTON_RIGHT) ? 1 : ((pressed & PAD_BUTTON_LEFT) ? -1 : 0);
            step = (held & PAD_BUTTON_X) ? 10 : 1;
            if (direction && debug_row == 0) debug_stat_actor = debug_wrap(debug_stat_actor + direction, 8);
            else if (direction && debug_row == 1) {
                if (!debug_stat_actor) {
                    pouch->currentHP = debug_clamp(pouch->currentHP + direction * step, 1, pouch->maximumHP);
                    if (debug_stat_locks & 1) debug_locked_values[0] = pouch->currentHP;
                } else {
                    PouchPartyData* partner = &pouch->partyData[debug_stat_actor];
                    partner->currentHP = debug_clamp(partner->currentHP + direction * step, 1, partner->maximumHP);
                }
                statusWinForceUpdate();
            } else if (direction && debug_row == 2) {
                if (!debug_stat_actor) {
                    pouch->baseMaxHP = debug_clamp(pouch->baseMaxHP + direction * step, 1, 99);
                    if (debug_stat_locks & 2) debug_locked_values[1] = pouch->baseMaxHP;
                    pouchReviseMarioParam();
                } else {
                    PouchPartyData* partner = &pouch->partyData[debug_stat_actor];
                    debug_partner_hp_override[debug_stat_actor] = debug_clamp(partner->baseMaxHP + direction * step, 1, 99);
                    debug_apply_partner_hp();
                }
                statusWinForceUpdate();
            } else if (direction && debug_row == 3)
                debug_attack_bonus[debug_stat_actor] = debug_clamp(debug_attack_bonus[debug_stat_actor] + direction * step, -10, 30);
            else if (direction && debug_row == 4)
                debug_defense_bonus[debug_stat_actor] = debug_clamp(debug_defense_bonus[debug_stat_actor] + direction * step, -10, 30);
            if ((pressed & PAD_TRIGGER_Z) && debug_row == 2 && debug_stat_actor && (held & chord) != chord) {
                debug_partner_hp_override[debug_stat_actor] = 0;
                pouchRevisePartyParam();
                debug_apply_partner_hp();
                statusWinForceUpdate();
            }
            if (pressed & PAD_BUTTON_B) { debug_open = 0; debug_consume = 1; }
            goto consume_buttons;
        }
        if (debug_page == 6) {
            s32 low = debug_item_kind ? BADGE_MIN : 0x80;
            s32 high = debug_item_kind ? BADGE_MAX - 1 : ITEM_MAX - 1;
            if (pressed & PAD_BUTTON_UP) debug_row = debug_wrap(debug_row - 1, 5);
            if (pressed & PAD_BUTTON_DOWN) debug_row = debug_wrap(debug_row + 1, 5);
            direction = (pressed & PAD_BUTTON_RIGHT) ? 1 : ((pressed & PAD_BUTTON_LEFT) ? -1 : 0);
            step = (held & PAD_BUTTON_Y) ? 100 : ((held & PAD_BUTTON_X) ? 10 : 1);
            if (direction && debug_row == 4) {
                PouchData* pouch = pouchGetPtr();
                pouch->mShineSpriteCount = debug_clamp((s32)pouch->mShineSpriteCount + direction * step, 0, 999);
                statusWinForceUpdate();
            }
            if (direction && debug_row == 0) {
                debug_item_kind = !debug_item_kind;
                debug_item_id = debug_item_kind ? BADGE_MIN : 0x80;
                debug_item_status = 0;
            } else if (direction && debug_row == 1) {
                debug_item_id = debug_clamp(debug_item_id + direction * step, low, high);
                debug_item_status = 0;
            }
            if ((pressed & PAD_BUTTON_A) && debug_row == 2)
                debug_item_status = pouchGetItem((ItemType)debug_item_id) ? 1 : 2;
            if ((pressed & PAD_BUTTON_A) && debug_row == 3) {
                debug_item_status = pouchRemoveItem((ItemType)debug_item_id) ? 1 : 2;
                if (debug_item_kind && debug_item_status == 1) { pouchReviseMarioParam(); pouchRevisePartyParam(); }
            }
            if (pressed & PAD_BUTTON_B) { debug_open = 0; debug_consume = 1; }
            goto consume_buttons;
        }
        if (debug_page == 5) {
            const char* target;
            s32 count;
            world = debug_world();
            area_count = debug_area_count();
            debug_area = debug_wrap(debug_area, area_count);
            area = world->areas[debug_area];
            room_count = debug_room_count(area);
            if (room_count <= 0) { debug_open = 0; goto consume_buttons; }
            debug_room = debug_wrap(debug_room, room_count);
            if (pressed & PAD_BUTTON_UP) debug_row = debug_wrap(debug_row - 1, 4);
            if (pressed & PAD_BUTTON_DOWN) debug_row = debug_wrap(debug_row + 1, 4);
            direction = (pressed & PAD_BUTTON_RIGHT) ? 1 : ((pressed & PAD_BUTTON_LEFT) ? -1 : 0);
            if (direction && debug_row == 0) { debug_area = debug_wrap(debug_area + direction, area_count); debug_room = 0; debug_entrance = -1; }
            area = world->areas[debug_area];
            room_count = debug_room_count(area);
            if (room_count <= 0) { debug_open = 0; goto consume_buttons; }
            if (direction && debug_row == 1) { debug_room = debug_wrap(debug_room + direction, room_count); debug_entrance = -1; }
            target = area->maps[debug_room]->mapName;
            count = debug_entrance_count(target);
            if (debug_entrance >= count) debug_entrance = -1;
            if (direction && debug_row == 2 && count) {
                debug_entrance += direction;
                if (debug_entrance < -1) debug_entrance = count - 1;
                if (debug_entrance >= count) debug_entrance = -1;
            }
            if ((pressed & PAD_BUTTON_A) && debug_row == 3 && debug_destination_available(target)) {
                const char* entrance = debug_entrance_current(target, debug_entrance);
                if (entrance && strlen(entrance) >= sizeof(debug_entrance_name)) goto consume_buttons;
                if (entrance) {
                    strncpy(debug_entrance_name, entrance, sizeof(debug_entrance_name) - 1);
                    debug_entrance_name[sizeof(debug_entrance_name) - 1] = 0;
                    entrance = debug_entrance_name;
                }
                seqSetSeq(SEQ_MAP_CHANGE, target, entrance);
                debug_open = 0; debug_consume = 1;
            }
            if (pressed & PAD_BUTTON_B) { debug_open = 0; debug_consume = 1; }
            goto consume_buttons;
        }
        if (debug_page == 4) {
            if (pressed & (PAD_BUTTON_UP | PAD_BUTTON_DOWN)) {
                debug_row = 1 - debug_row;
                debug_preset_confirm = 0;
            }
            if (debug_row == 0) {
                direction = (pressed & PAD_BUTTON_RIGHT) ? 1 : ((pressed & PAD_BUTTON_LEFT) ? -1 : 0);
                step = (held & PAD_BUTTON_Y) ? 100 : ((held & PAD_BUTTON_X) ? 10 : 1);
                if (direction) { debug_preset_id = debug_clamp(debug_preset_id + direction * step, 0, 9999); debug_preset_confirm = 0; }
                if (pressed & PAD_BUTTON_A) {
                    EventData* event = debug_story_event(debug_preset_id, TRUE);
                    debug_preset_id = event ? event->id : 0;
                    debug_preset_confirm = 0;
                }
            } else if (pressed & PAD_BUTTON_A) {
                if (!debug_preset_confirm) { debug_preset_confirm = 1; debug_preset_error = 0; }
                else if (debug_apply_preset(debug_preset_id)) { debug_open = 0; debug_consume = 1; debug_preset_confirm = 0; }
                else { debug_preset_error = 1; debug_preset_confirm = 0; }
            }
            if (pressed & PAD_BUTTON_B) { debug_open = 0; debug_consume = 1; debug_preset_confirm = 0; }
            goto consume_buttons;
        }
        if (debug_page == 3) {
            if (pressed & PAD_BUTTON_UP) debug_row = debug_wrap(debug_row - 1, 3);
            if (pressed & PAD_BUTTON_DOWN) debug_row = debug_wrap(debug_row + 1, 3);
            if (debug_row == 2) {
                if (pressed & PAD_BUTTON_LEFT) debug_cam_speed = debug_clamp(debug_cam_speed - 1, 1, 5);
                if (pressed & PAD_BUTTON_RIGHT) debug_cam_speed = debug_clamp(debug_cam_speed + 1, 1, 5);
            }
            if ((pressed & PAD_BUTTON_A) && debug_row < 2) {
                if (debug_row == 0) {
                    debug_freecam = !debug_freecam;
                    if (debug_freecam) {
                        CameraEntry* camera = camGetPtr(CAMERA_3D);
                        debug_freecam_start(camera);
                    }
                } else {
                    debug_wallpass = !debug_wallpass;
                    debug_wall_update();
                }
            }
            if (pressed & PAD_BUTTON_B) { debug_open = 0; debug_consume = 1; }
            goto consume_buttons;
        }
        if (debug_page == 2) {
            if (pressed & PAD_BUTTON_UP) debug_row = debug_wrap(debug_row - 1, 8);
            if (pressed & PAD_BUTTON_DOWN) debug_row = debug_wrap(debug_row + 1, 8);
            direction = (pressed & PAD_BUTTON_RIGHT) ? 1 : ((pressed & PAD_BUTTON_LEFT) ? -1 : 0);
            step = (held & PAD_BUTTON_Y) ? 100 : ((held & PAD_BUTTON_X) ? 10 : 1);
            if (direction) debug_change_stat(debug_row, direction * step);
            if ((pressed & PAD_TRIGGER_Z) && debug_row < 7 && (held & chord) != chord) {
                u32 bit = 1u << debug_row;
                if (!(debug_stat_locks & bit))
                    debug_locked_values[debug_row] = debug_read_stat(pouchGetPtr(), debug_row);
                debug_stat_locks ^= bit;
            }
            if ((pressed & PAD_BUTTON_A) && debug_row == 7) {
                if (debug_start_save()) { debug_freecam = 0; debug_open = 0; debug_consume = 1; }
                else debug_save_error = 1;
            }
            if (pressed & PAD_BUTTON_B) { debug_open = 0; debug_consume = 1; }
            goto consume_buttons;
        }
        if (debug_page == 1) {
            if (pressed & PAD_BUTTON_UP) debug_row = debug_wrap(debug_row - 1, 8);
            if (pressed & PAD_BUTTON_DOWN) debug_row = debug_wrap(debug_row + 1, 8);
            if (debug_row == 0) {
                if (pressed & PAD_BUTTON_LEFT) debug_character = debug_wrap(debug_character - 1, 3);
                if (pressed & PAD_BUTTON_RIGHT) debug_character = debug_wrap(debug_character + 1, 3);
                if ((pressed & PAD_BUTTON_A) && marioGetPtr()->characterId != debug_character &&
                    (debug_character == 0 || marioGetParty() == 0))
                    marioSetCharMode(debug_character);
            } else if (pressed & PAD_BUTTON_A) {
                debug_advance_partner((PartyId)debug_row);
            }
            if ((pressed & PAD_TRIGGER_Z) && (held & chord) != chord)
                debug_dismiss_partner();
            if (pressed & PAD_BUTTON_B) { debug_open = 0; debug_consume = 1; }
            goto consume_buttons;
        }
        world = debug_world();
        area_count = debug_area_count();
        if (area_count <= 0) { debug_open = 0; return; }
        debug_area = debug_wrap(debug_area, area_count);
        area = world->areas[debug_area];
        room_count = debug_room_count(area);
        if (room_count <= 0) { debug_open = 0; return; }
        debug_room = debug_wrap(debug_room, room_count);
        if (pressed & PAD_BUTTON_UP) debug_row = debug_wrap(debug_row - 1, 8);
        if (pressed & PAD_BUTTON_DOWN) debug_row = debug_wrap(debug_row + 1, 8);
        direction = (pressed & PAD_BUTTON_RIGHT) ? 1 : ((pressed & PAD_BUTTON_LEFT) ? -1 : 0);
        step = (held & PAD_BUTTON_Y) ? 100 : ((held & PAD_BUTTON_X) ? 10 : 1);
        if (direction) {
            switch (debug_row) {
                case 0: {
                    s32 value = swByteGet(0) + direction * step;
                    if (value < 0) value = 0;
                    if (value > 9999) value = 9999;
                    swByteSet(0, value);
                    break;
                }
                case 1:
                    debug_byte += direction * step;
                    if (debug_byte < 1) debug_byte = 1;
                    if (debug_byte >= 0x800) debug_byte = 0x7ff;
                    break;
                case 2: {
                    s32 value = swByteGet(debug_byte) + direction * step;
                    if (value < 0) value = 0;
                    if (value > 255) value = 255;
                    swByteSet(debug_byte, value);
                    break;
                }
                case 3:
                    debug_flag += direction * step;
                    if (debug_flag < 0) debug_flag = 0;
                    if (debug_flag >= 8192) debug_flag = 8191;
                    break;
                case 5:
                    debug_area = debug_wrap(debug_area + direction, area_count);
                    debug_room = 0;
                    break;
                case 6:
                    debug_room = debug_wrap(debug_room + direction, room_count);
                    break;
            }
        }
        if ((pressed & PAD_BUTTON_A) && debug_row == 0) {
            EventData* event = debug_story_event(swByteGet(0), TRUE);
            swByteSet(0, event ? event->id : 0);
        }
        /* Z selects the story table's own destination and entrance. Do not
         * treat Z from the opening chord as a request to warp. */
        if ((pressed & PAD_TRIGGER_Z) && debug_row == 0 && (held & chord) != chord) {
            EventData* event = debug_story_event(swByteGet(0), FALSE);
            if (event && event->mapName && mapDataPtr(event->mapName) &&
                debug_destination_available(event->mapName)) {
                EventData* previous = debug_story_event(event->id, 2);
                swByteSet(0, previous ? previous->id : 0);
                seqSetSeq(SEQ_MAP_CHANGE, event->mapName, event->beroName);
                debug_open = 0;
                debug_consume = 1;
            }
        }
        if ((pressed & PAD_BUTTON_A) && debug_row == 3)
            debug_flag = debug_next_known_flag(debug_flag);
        if ((pressed & PAD_BUTTON_A) && debug_row == 4) {
            if (swGet(debug_flag)) swClear(debug_flag); else swSet(debug_flag);
        }
        if ((pressed & PAD_BUTTON_A) && debug_row == 7) {
            const char* map = world->areas[debug_area]->maps[debug_room]->mapName;
            const char* entrance = NULL;
            if (debug_destination_available(map)) {
                /* These entrances are used by the game's own loading/debug code. */
                if (!strcmp(map, "aaa_00")) entrance = "prologue";
                else if (!strcmp(map, "hei_00")) entrance = "dokan_2";
                seqSetSeq(SEQ_MAP_CHANGE, map, entrance);
                debug_open = 0;
                debug_consume = 1;
            }
        }
        if (pressed & PAD_BUTTON_B) { debug_open = 0; debug_consume = 1; }
    }
consume_buttons:
    if (debug_freecam && !debug_open) debug_freecam_move();
    if (debug_open || debug_consume || debug_freecam) {
        gp->button[0] = gp->buttonNew[0] = gp->buttonRepeat[0] = gp->buttonUp[0] = 0;
        gp->dirs[0] = gp->dirsNew[0] = gp->dirsRepeat[0] = 0;
        gp->stickX[0] = gp->stickY[0] = gp->substickX[0] = gp->substickY[0] = 0;
        gp->triggerLeft[0] = gp->triggerRight[0] = 0;
        if (!debug_open && held == 0) debug_consume = 0;
    }
}

static void debug_menu_draw(CameraId camera, void* param) {
    char text[96];
    WorldData* world = debug_world();
    AreaData* area = world->areas[debug_area];
    s32 i;
    (void)camera; (void)param;
    FontDrawStart();
    FontDrawEdge();
    FontDrawScale(0.75f);
    FontDrawColor((GXColor){255,255,255,255});
    if (debug_page == 7) {
        PouchData* pouch = pouchGetPtr();
        PouchPartyData* partner = &pouch->partyData[debug_stat_actor];
        FontDrawString(-280.0f, 200.0f, "CHARACTER STATS  (L: PAGE)");
        for (i = 0; i < 5; ++i) {
            const char* select = i == debug_row ? ">" : " ";
            FontDrawColor(i == debug_row ? (GXColor){255,230,64,255} : (GXColor){255,255,255,255});
            if (i == 0) sprintf(text, "%s CHARACTER: %s", select, debug_stat_actor ? debug_partners[debug_stat_actor - 1] : "MARIO");
            else if (i == 1) sprintf(text, "%s HP: %d / %d", select, debug_stat_actor ? partner->currentHP : pouch->currentHP, debug_stat_actor ? partner->maximumHP : pouch->maximumHP);
            else if (i == 2) sprintf(text, "%s BASE MAX HP: %d", select, debug_stat_actor ? partner->baseMaxHP : pouch->baseMaxHP);
            else if (i == 3) sprintf(text, "%s DAMAGE BONUS: %d", select, debug_attack_bonus[debug_stat_actor]);
            else sprintf(text, "%s DAMAGE REDUCTION: %d", select, debug_defense_bonus[debug_stat_actor]);
            FontDrawString(-280.0f, 164.0f - 24.0f * i, text);
        }
        FontDrawColor((GXColor){255,255,255,255});
        FontDrawString(-280.0f, 45.0f, "LEFT/RIGHT: CHANGE    X: x10");
        FontDrawString(-280.0f, 20.0f, "Z ON PARTNER MAX HP: RESET TO RANK.");
        FontDrawString(-280.0f, -5.0f, "BONUSES AFFECT NORMAL BATTLE DAMAGE.");
        FontDrawString(-280.0f, -30.0f, "BONUSES AND CUSTOM MAX HP ARE TEMPORARY.");
        return;
    }
    if (debug_page == 6) {
        const char* name = itemDataTable[debug_item_id].name;
        const char* title = name ? msgSearch(name) : NULL;
        FontDrawString(-280.0f, 200.0f, "INVENTORY  (L: PAGE)");
        for (i = 0; i < 5; ++i) {
            const char* select = i == debug_row ? ">" : " ";
            FontDrawColor(i == debug_row ? (GXColor){255,230,64,255} : (GXColor){255,255,255,255});
            if (i == 0) sprintf(text, "%s CATEGORY: %s", select, debug_item_kind ? "BADGES" : "ITEMS");
            else if (i == 1) sprintf(text, "%s ID %d: %.38s", select, debug_item_id, title ? title : "UNKNOWN");
            else if (i == 2) sprintf(text, "%s ADD ONE (A)", select);
            else if (i == 3) sprintf(text, "%s REMOVE ONE (A)", select);
            else sprintf(text, "%s SHINE SPRITES: %d", select, pouchGetPtr()->mShineSpriteCount);
            FontDrawString(-280.0f, 164.0f - 24.0f * i, text);
        }
        FontDrawColor((GXColor){255,255,255,255});
        sprintf(text, "IN BAG: %d", pouchCheckItem(debug_item_id));
        FontDrawString(-280.0f, 45.0f, text);
        FontDrawString(-280.0f, 20.0f, "LEFT/RIGHT: SELECT  X: x10  Y: x100");
        if (debug_item_status) FontDrawString(-280.0f, -5.0f, debug_item_status == 1 ? "DONE" : "NOT ADDED / NOT FOUND");
        FontDrawString(-280.0f, -30.0f, "KEY ITEMS ARE NOT EDITABLE HERE.");
        return;
    }
    if (debug_page == 5) {
        const char* target = area->maps[debug_room]->mapName;
        const char* entrance = debug_entrance_current(target, debug_entrance);
        FontDrawString(-280.0f, 200.0f, "ROOM ENTRANCES  (L: PAGE)");
        for (i = 0; i < 4; ++i) {
            const char* select = i == debug_row ? ">" : " ";
            FontDrawColor(i == debug_row ? (GXColor){255,230,64,255} : (GXColor){255,255,255,255});
            if (i == 0) sprintf(text, "%s AREA: %s", select, debug_area < 33 ? debug_area_names[debug_area] : area->areaName);
            else if (i == 1) sprintf(text, "%s MAP: %s", select, target);
            else if (i == 2) sprintf(text, "%s ENTRANCE: %.35s", select, entrance ? entrance : "DEFAULT");
            else sprintf(text, "%s %s", select, debug_destination_available(target) ? "WARP (A)" : "UNAVAILABLE - MISSING FILES");
            FontDrawString(-280.0f, 164.0f - 24.0f * i, text);
        }
        FontDrawColor((GXColor){255,255,255,255});
        FontDrawString(-280.0f, 45.0f, "NAMED ENTRANCES: CURRENT ROOM ONLY.");
        FontDrawString(-280.0f, 20.0f, "LOAD A ROOM FIRST TO SEE ITS ENTRANCES.");
        return;
    }
    if (debug_page == 4) {
        EventData* event = debug_story_event(debug_preset_id, FALSE);
        FontDrawString(-280.0f, 200.0f, "STORY PRESETS  (L: PAGE)");
        FontDrawColor(debug_row == 0 ? (GXColor){255,230,64,255} : (GXColor){255,255,255,255});
        sprintf(text, "%s EVENT: %d (A: NEXT)", debug_row == 0 ? ">" : " ", debug_preset_id);
        FontDrawString(-280.0f, 164.0f, text);
        sprintf(text, "   %.45s", event && event->nameEn ? event->nameEn : "UNKNOWN POSITION");
        FontDrawString(-280.0f, 140.0f, text);
        FontDrawColor(debug_row == 1 ? (GXColor){255,230,64,255} : (GXColor){255,255,255,255});
        sprintf(text, "%s %s", debug_row == 1 ? ">" : " ", debug_preset_confirm ? "A AGAIN: CONFIRM RESET" : "APPLY PRESET (A)");
        FontDrawString(-280.0f, 105.0f, text);
        FontDrawColor((GXColor){255,255,255,255});
        sprintf(text, "DESTINATION: %.35s", event && event->mapName ? event->mapName : "UNKNOWN");
        FontDrawString(-280.0f, 78.0f, text);
        FontDrawString(-280.0f, 50.0f, "RESETS FLAGS, INVENTORY AND PARTNERS!");
        FontDrawString(-280.0f, 25.0f, "BASED ON GAME DEMO SETUP; BACK UP SAVE.");
        if (debug_preset_error) FontDrawString(-280.0f, 0.0f, "NOT AVAILABLE OR GAME IS BUSY.");
        return;
    }
    if (debug_page == 3) {
        FontDrawString(-280.0f, 200.0f, "EXPLORATION  (L: PAGE)");
        for (i = 0; i < 3; ++i) {
            const char* select = i == debug_row ? ">" : " ";
            FontDrawColor(i == debug_row ? (GXColor){255,230,64,255} : (GXColor){255,255,255,255});
            if (i == 0) sprintf(text, "%s FREE CAMERA: %s  (A)", select, debug_freecam ? "ON" : "OFF");
            else if (i == 1) sprintf(text, "%s PASS WALLS: %s  (A)", select, debug_wallpass ? "ON" : "OFF");
            else sprintf(text, "%s CAMERA SPEED: x%d  (LEFT/RIGHT)", select, debug_cam_speed);
            FontDrawString(-280.0f, 164.0f - 24.0f * i, text);
        }
        FontDrawColor((GXColor){255,255,255,255});
        FontDrawString(-280.0f, 80.0f, "CLOSE MENU TO MOVE CAMERA:");
        FontDrawString(-280.0f, 55.0f, "LEFT STICK: MOVE   C-STICK: LOOK");
        FontDrawString(-280.0f, 30.0f, "L / R: DOWN / UP");
        FontDrawString(-280.0f, 5.0f, "REOPEN MENU TO DISABLE FREE CAMERA.");
        FontDrawString(-280.0f, -20.0f, "WALL MODE KEEPS GROUND CHECKS.");
        return;
    }
    if (debug_page == 2) {
        PouchData* pouch = pouchGetPtr();
        FontDrawString(-280.0f, 200.0f, "STATS / SAVE  (L: PAGE)");
        for (i = 0; i < 8; ++i) {
            const char* select = i == debug_row ? ((debug_stat_locks & (1u << i)) ? ">*" : "> ") :
                                                  ((debug_stat_locks & (1u << i)) ? " *" : "  ");
            FontDrawColor(i == debug_row ? (GXColor){255,230,64,255} : (GXColor){255,255,255,255});
            switch (i) {
                case 0: sprintf(text, "%s HP: %d / %d", select, pouch->currentHP, pouch->maximumHP); break;
                case 1: sprintf(text, "%s BASE MAX HP: %d", select, pouch->baseMaxHP); break;
                case 2: sprintf(text, "%s FP: %d / %d", select, pouch->currentFP, pouch->maximumFP); break;
                case 3: sprintf(text, "%s BASE MAX FP: %d", select, pouch->baseMaxFP); break;
                case 4: sprintf(text, "%s BP TOTAL: %d (FREE: %d)", select, pouch->maximumBP, pouch->availableBP); break;
                case 5: sprintf(text, "%s COINS: %d", select, pouch->coins); break;
                case 6: sprintf(text, "%s STAR PIECES: %d", select, pouch->mStarPieceCount); break;
                default: sprintf(text, "%s SAVE GAME (A)", select); break;
            }
            FontDrawString(-280.0f, 164.0f - 24.0f * i, text);
        }
        FontDrawColor((GXColor){255,255,255,255});
        FontDrawString(-280.0f, -55.0f, "LEFT/RIGHT: CHANGE    X: x10    Y: x100");
        FontDrawString(-280.0f, -80.0f, "Z: LOCK / UNLOCK   * = LOCKED");
        FontDrawString(-280.0f, -105.0f, "MAX HP / FP ARE BEFORE BADGE BONUSES.");
        if (debug_save_error) FontDrawString(-280.0f, -130.0f, "SAVE BUSY - TRY AGAIN WHEN GAME IS IDLE.");
        return;
    }
    if (debug_page == 1) {
        FontDrawString(-280.0f, 200.0f, "CHARACTERS / PARTNERS  (L: PAGE)");
        for (i = 0; i < 8; ++i) {
            const char* select = i == debug_row ? ">" : " ";
            FontDrawColor(i == debug_row ? (GXColor){255,230,64,255} : (GXColor){255,255,255,255});
            if (i == 0)
                sprintf(text, "%s CHARACTER: %s (A: APPLY)", select, debug_characters[debug_character]);
            else {
                s32 level = pouchGetPtr()->partyData[i].techLevel;
                const char* name = !partyChkJoin((PartyId)i) ? "OFF" :
                    (level >= 0 && level <= 2 ? debug_partner_levels[level] : "UNKNOWN");
                sprintf(text, "%s %s: %s", select, debug_partners[i - 1], name);
            }
            FontDrawString(-280.0f, 164.0f - 24.0f * i, text);
        }
        FontDrawColor((GXColor){255,255,255,255});
        FontDrawString(-280.0f, -55.0f, "A: APPLY / NEXT RANK   Z: DISMISS PARTNER");
        FontDrawString(-280.0f, -80.0f, "PARTNERS: OFF / NORMAL / SUPER / ULTRA");
        FontDrawString(-280.0f, -105.0f, "DISMISS PARTNER BEFORE PEACH / BOWSER.");
        FontDrawString(-280.0f, -130.0f, "SOME MAPS REQUIRE A SPECIFIC CHARACTER.");
        i = marioGetPtr()->characterId;
        sprintf(text, "CURRENT CHARACTER: %s", (i >= 0 && i < 3) ? debug_characters[i] : "UNKNOWN");
        FontDrawString(-280.0f, -155.0f, text);
        return;
    }
    FontDrawString(-280.0f, 200.0f, "TTYD STATE / WARP  (L: PAGE)");
    for (i = 0; i < 8; ++i) {
        const char* select = i == debug_row ? ">" : " ";
        FontDrawColor(i == debug_row ? (GXColor){255, 230, 64, 255} : (GXColor){255, 255, 255, 255});
        switch (i) {
            case 0: sprintf(text, "%s STORY: %d (A: NEXT  Z: WARP)", select, swByteGet(0)); break;
            case 1: sprintf(text, "%s GLOBAL BYTE INDEX: %d", select, debug_byte); break;
            case 2: sprintf(text, "%s GLOBAL BYTE VALUE: %d", select, swByteGet(debug_byte)); break;
            case 3: sprintf(text, "%s FLAG INDEX: %d  (A: NEXT KNOWN)", select, debug_flag); break;
            case 4: sprintf(text, "%s GLOBAL FLAG: %s  (A TO TOGGLE)", select, swGet(debug_flag) ? "ON" : "OFF"); break;
            case 5: sprintf(text, "%s AREA: %s", select, debug_area < 33 ? debug_area_names[debug_area] : area->areaName); break;
            case 6: {
                const char* room_name = debug_room_name(debug_area, debug_room);
                if (room_name) sprintf(text, "%s MAP: %s (%s)", select, room_name, area->maps[debug_room]->mapName);
                else sprintf(text, "%s MAP: %s", select, area->maps[debug_room]->mapName);
                break;
            }
            default:
                if (debug_destination_available(area->maps[debug_room]->mapName))
                    sprintf(text, "%s WARP TO SELECTED MAP  (A)", select);
                else
                    sprintf(text, "%s UNAVAILABLE - MISSING DISC FILES", select);
                break;
        }
        FontDrawString(-280.0f, 164.0f - 24.0f * i, text);
    }
    FontDrawColor((GXColor){255, 255, 255, 255});
    if (debug_row == 0) {
        EventData* event = debug_story_event(swByteGet(0), FALSE);
        sprintf(text, "STORY: %.45s", event && event->nameEn ? event->nameEn : "UNKNOWN POSITION");
    } else {
        sprintf(text, "FLAG %d: %s", debug_flag, debug_flag_name(debug_flag));
    }
    FontDrawString(-280.0f, -55.0f, text);
    FontDrawString(-280.0f, -80.0f, "D-PAD: SELECT / CHANGE   X: x10   Y: x100");
    FontDrawString(-280.0f, -105.0f, "RAW STATE! BACK UP YOUR SAVE BEFORE EDITING.");
    FontDrawString(-280.0f, -130.0f, "MOST MAPS USE ORIGIN; SPAWN MAY BE UNSAFE.");
}

static void debug_menu_enqueue(void) {
    if (debug_open && seqGetSeq() == SEQ_GAME && !seqCheckSeq())
        dispEntry(CAMERA_2D, -9999.0f, 3, debug_menu_draw, NULL);
}

void debug_input_hook(void) {
    makeKey();
    debug_menu_input();
}
void debug_draw_hook(void) {
    effMain();
    debug_apply_partner_hp();
    debug_apply_stat_locks();
    debug_menu_enqueue();
}


/* OSInit may lower the arena to the regular stack end and erase the
 * debugger stack. Reserve space for the mod before the game clears or allocates the arena. */
void debug_arena_lo_hook(void* arena) {
    if ((u32)arena < 0x80441000u) arena = (void*)0x80441000u;
    OSSetArenaLo(arena);
}
