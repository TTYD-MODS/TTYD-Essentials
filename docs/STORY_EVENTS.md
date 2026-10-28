# Story event reference

Generated from the US story tables in `src/event.c` by `python3 tools/debugmod/index_story.py /path/to/upstream`. IDs are the game's event sequence values; some values have multiple entries. The game's own demo initializer sometimes sets progress to the preceding event ID before loading a selected event. Changing the raw progress value alone does not initialize inventory, partners, other flags, or a destination.

| ID | Event | Area | Entrance |
| ---: | --- | --- | --- |
| 0 | Prologue | `aaa_00` | `prologue` |
| 1 | Plaza | `aaa_00` | `prologue` |
| 2 | Mario's House | `aaa_00` | `prologue` |
| 3 | To Rogueport | `sys_01` | `prologue` |
| 3 | Rogueport (Arrival) | `gor_00` | `` |
| 4 | Goombella Assaulted | `gor_00` | `` |
| 5 | 1000 X-Nauts (Before) | `gor_00` | `` |
| 6 | 1000 X-Nauts (After) | `gor_00` | `` |
| 7 | Goombella Joins | `gor_01` | `s_bero` |
| 8 | Stolen Coins | `gor_02` | `w_bero` |
| 9 | Prof. Frankly | `gor_02` | `w_bero` |
| 10 | Removing the Fence | `gor_02` | `w_bero` |
| 11 | Frankly's Tutorial | `gor_02` | `w_bero` |
| 12 | 3 Goomba Goons | `tik_01` | `dokan_2` |
| 13 | Puni Encounter | `tik_04` | `dokan` |
| 14 | Paper Stair Switch | `tik_04` | `dokan` |
| 15 | Paper Mage 1 | `tik_19` | `s_bero` |
| 16 | First Flight | `tik_04` | `n_bero_5` |
| 16 | Thousand-Year Door | `tik_05` | `e_bero` |
| 17 | Front of the Pedestal | `tik_05` | `e_bero` |
| 18 | The Pedestal | `tik_05` | `e_bero` |
| 19 | Frankly's House | `gor_02` | `` |
| 20 | Badge Tutorial | `gor_02` | `w_bero` |
| 21 | Blooper Battle | `tik_02` | `w_bero_1` |
| 22 | To Stage 1 | `tik_02` | `w_bero_1` |
| 23 | Petal Meadows | `sys_01` | `stg_1` |
| 24 | The Shadow of Hooktail | `hei_00` | `dokan_2` |
| 25 | The Flip-Bridge | `hei_01` | `w_bero` |
| 26 | Petalburg (1st Time) | `nok_00` | `w_bero` |
| 27 | Talking with Kroop | `nok_01` | `w_bero` |
| 28 | Petalburg Gatekeeper | `nok_01` | `w_bero` |
| 29 | Bald Cleft | `hei_03` | `w_bero` |
| 30 | Bristle | `hei_05` | `w_bero` |
| 31 | Quiz | `hei_07` | `w_bero` |
| 32 | Gold Fuzzy | `hei_10` | `w_bero` |
| 33 | Koops Joins | `hei_01` | `e_bero` |
| 34 | Opening the Path | `hei_00` | `e_bero` |
| 35 | Hooktail Castle | `gon_01` | `w_bero_1` |
| 36 | Key | `gon_01` | `w_bero_1` |
| 37 | Lock | `gon_01` | `w_bero_1` |
| 38 | Father's Letter | `gon_03` | `w_bero` |
| 39 | 1000 Dry Bones | `gon_03` | `w_bero` |
| 40 | Paper Stairs | `gon_04` | `w_bero_1` |
| 41 | Key | `gon_04` | `w_bero_1` |
| 42 | Lock | `gon_04` | `w_bero_1` |
| 43 | A Suspicious Room | `gon_07` | `w_bero` |
| 44 | 50 Seconds to Escape | `gon_06` | `e_bero` |
| 45 | Paper Mage 2 | `gon_06` | `e_bero` |
| 46 | Key 2 | `gon_03` | `e_bero` |
| 47 | Lock 2 | `gon_05` | `w_bero_1` |
| 48 | Paper Bridge (Right) | `gon_04` | `e_bero_3` |
| 49 | Paper Bridge (Left) | `gon_04` | `e_bero_3` |
| 50 | Ms. Mowz (w/Goombella) | `gon_12` | `e_bero` |
| 50 | Ms. Mowz (w/Koops) | `gon_12` | `e_bero` |
| 51 | Key 3 | `gon_12` | `e_bero` |
| 52 | Lock 3 | `gon_08` | `w_bero` |
| 53 | Key 4 | `gon_05` | `w_bero_4` |
| 54 | Lock 4 | `gon_05` | `w_bero_4` |
| 55 | Hooktail | `gon_11` | `w_bero` |
| 55 | Hooktail Defeated | `gon_11` | `` |
| 56 | Father & Son Reunited | `gon_11` | `w_bero` |
| 57 | Peach: Caught | `aji_10` | `` |
| 58 | Peach: An Open Door | `aji_16` | `` |
| 59 | Peach: TEC | `aji_17` | `w_bero` |
| 60 | Bowser: Bowser Castle | `kpa_00` | `` |
| 60 | Bowser: Entrance | `kpa_01` | `` |
| 61 | Bowser: Castle INT. | `kpa_01` | `player` |
| 61 | Bowser: Kammy Enters | `kpa_01` | `event` |
| 61 | Bowser: Departure | `kpa_00` | `` |
| 62 | Koops Leaves | `nok_01` | `nokotarou` |
| 63 | A Mail from Peach | `hei_01` | `e_bero` |
| 64 | Zess T. | `gor_01` | `e_bero` |
| 64 | Thousand-Year Door | `tik_05` | `e_bero` |
| 65 | Frankly's House Stg.1 | `gor_02` | `` |
| 66 | Puni Encounter 2 | `tik_04` | `dokan` |
| 67 | A Puni Plea for Help | `tik_03` | `s_bero_3` |
| 68 | Puni's Secret Passage | `tik_03` | `s_bero_3` |
| 69 | Puni Joins | `tik_03` | `s_bero_3` |
| 70 | To Stage 2 | `tik_03` | `a_slit` |
| 71 | Boggly Woods | `sys_01` | `stg_2` |
| 72 | A Siren Argument | `win_00` | `w_bero` |
| 73 | To The Great Tree | `win_01` | `w_bero` |
| 74 | The Great Tree | `mri_00` | `w_bero` |
| 75 | Sealed Entrance | `mri_00` | `w_bero` |
| 76 | Sealed Entrance 2 | `mri_00` | `w_bero` |
| 77 | Flurrie Intro | `win_03` | `` |
| 78 | She's Lost Her Precious | `win_03` | `` |
| 79 | To Flurrie's Place | `win_01` | `n_bero` |
| 80 | Extending Plane Panel | `win_02` | `w_bero` |
| 80 | The Trail | `win_03` | `w_bero` |
| 81 | A Shy Flurrie | `win_04` | `w_bero` |
| 82 | Flurrie: Living Room | `win_04` | `w_bero` |
| 83 | Flurrie: Request | `win_04` | `w_bero` |
| 84 | The Sketch | `win_00` | `` |
| 85 | Mario vs. Shadow Sirens | `win_00` | `e_bero` |
| 86 | Shadow Sirens Lose | `win_00` | `` |
| 87 | Flurrie Joins | `win_04` | `w_bero` |
| 88 | Secret Entrance Revealed! | `mri_00` | `w_bero` |
| 89 | X-Naut Battle | `mri_01` | `w_bero` |
| 90 | Rival Arrival | `mri_01` | `` |
| 91 | A Dark Figure | `mri_04` | `` |
| 92 | Puni Elder Imprisoned | `mri_03` | `dokan` |
| 93 | Ms. Mowz | `mri_04` | `e_bero` |
| 94 | Puni Elder Freed | `mri_03` | `w_bero` |
| 95 | 11 Punies | `mri_01` | `dokan` |
| 96 | The Puni Elder's Powers | `mri_01` | `w_bero` |
| 96 | Puni Switch | `mri_02` | `dokan1` |
| 97 | Bubbles | `mri_05` | `dokan3` |
| 97 | By Plane? | `mri_19` | `dokan1` |
| 97 | Jabbi Encounter | `mri_06` | `dokan1` |
| 98 | Jabble | `mri_07` | `e_bero` |
| 98 | Punies vs. Jabbies | `mri_08` | `w_bero` |
| 98 | Blue Key Obtained | `mri_09` | `w_bero` |
| 99 | Inside the Blue Cell | `mri_03` | `` |
| 100 | Punio & Petuni(Before) | `mri_03` | `dokan` |
| 101 | Punio & Petuni | `mri_03` | `dokan` |
| 102 | Bubbles 2 | `mri_05` | `dokan3` |
| 102 | Punies vs. Jabbies 2 | `mri_11` | `e_bero` |
| 102 | Trapped | `mri_17` | `w_bero` |
| 103 | Mystery Pillar | `mri_17` | `w_bero` |
| 104 | Matching the Patterns | `mri_09` | `w_bero` |
| 105 | Super Boots | `mri_10` | `s_bero` |
| 106 | Escape | `mri_17` | `w_bero` |
| 107 | Water Switch | `mri_16` | `dokan2` |
| 107 | The 101 Puni Switch | `mri_13` | `dokan` |
| 108 | Lord Crump Appears | `mri_14` | `` |
| 109 | Time Bomb Activated | `mri_14` | `w_bero` |
| 110 | X-Naut Battle | `mri_15` | `dokan` |
| 111 | Boss Battle | `mri_01` | `e_bero` |
| 112 | After the Boss Battle | `mri_01` | `` |
| 113 | Peach: Crump & X-Nauts | `aji_10` | `` |
| 113 | Peach: An Open Door 2 | `aji_16` | `` |
| 114 | Peach: Shall We Dance? | `aji_17` | `w_bero` |
| 115 | Bowser: Meadows | `hei_00` | `` |
| 116 | Bowser: Action Stage | `kpa_02` | `` |
| 117 | Bowser: Petalburg | `nok_00` | `w_bero` |
| 118 | Praise from the Puni | `mri_00` | `` |
| 119 | A Mail from Peach | `win_01` | `dokan1` |
| 120 | Thousand-Year Door | `tik_05` | `e_bero` |
| 121 | Frankly's House Stg.2 | `gor_02` | `` |
| 122 | Finding Don Pianta | `gor_02` | `w_bero` |
| 122 | Backdoor | `gor_03` | `e_bero` |
| 122 | Mafia Boss | `gor_03` | `` |
| 123 | Daughter Located | `gor_00` | `n_bero` |
| 124 | Blimp Ticket | `gor_03` | `` |
| 125 | After Getting the Ticket | `gor_03` | `` |
| 126 | To Glitzville | `gor_04` | `s_bero` |
| 127 | Welcome to Glitzville | `tou_20` | `start` |
| 128 | Arena Intro (1F) | `tou_03` | `s_bero_1` |
| 128 | Arena Intro (2F) | `tou_03` | `s_bero_2` |
| 129 | The Guard Backs Off | `tou_02` | `s_bero` |
| 130 | Grubba | `tou_05` | `n_bero` |
| 131 | Gonzales is Born | `tou_05` | `n_bero` |
| 132 | Match | `tou_10` | `` |
| 133 | 1st Match | `tou_03` | `` |
| 134 | Minors - 9th Pl. | `tou_10` | `n_bero` |
| 134 | Minors - 8th Pl. | `tou_10` | `n_bero` |
| 134 | Minors - 7th Pl. | `tou_10` | `n_bero` |
| 134 | Minors - 6th Pl. | `tou_10` | `n_bero` |
| 135 | Minors - 5th Pl. (Egg) | `tou_01` | `a_door_mon` |
| 136 | Runaway Egg | `tou_01` | `a_door_mon` |
| 137 | The Mini-Yoshi Egg | `tou_01` | `a_door_mon` |
| 137 | Minors - 4th Pl. | `tou_10` | `n_bero` |
| 137 | Minors - 3rd Pl. | `tou_10` | `n_bero` |
| 137 | Minors - 2nd Place | `tou_10` | `n_bero` |
| 137 | Minors - 1st Pl. (Iron) | `tou_10` | `n_bero` |
| 137 | Minors - 1st Pl. (Iron 2) | `tou_10` | `n_bero` |
| 138 | Majors - 10th Place | `tou_08` | `n_bero` |
| 138 | Majors - 9th Place | `tou_08` | `n_bero` |
| 139 | Majors - 8th Place | `tou_08` | `n_bero` |
| 140 | Super Hammer | `tou_01` | `a_door_mon` |
| 141 | Back to the Minors | `tou_04` | `e_bero` |
| 142 | The Yellow Block | `tou_10` | `n_bero` |
| 143 | Confiscated | `tou_10` | `n_bero` |
| 143 | Majors - 7th Pl.(Raid/Cake) | `tou_08` | `n_bero` |
| 143 | Majors - 6th Pl.(Bowser) | `tou_08` | `n_bero` |
| 143 | Majors - 5th Pl. | `tou_08` | `n_bero` |
| 144 | Majors - 4th Pl. | `tou_08` | `n_bero` |
| 145 | Rawk Hawk's Warning | `tou_04` | `s_bero_6` |
| 146 | Storage Key | `tou_01` | `a_door_mon` |
| 147 | Storage Room Unlocked | `tou_04` | `e_bero` |
| 148 | Ms. Mowz | `tou_06` | `n_bero` |
| 149 | Blowing Containers | `tou_06` | `n_bero` |
| 150 | Hidden Stairway | `tou_06` | `n_bero` |
| 151 | Hole in the Floor | `tou_06` | `n_bero` |
| 152 | Jolene's Secret | `tou_05` | `fall` |
| 152 | Majors - 3rd Pl.(Poison) | `tou_08` | `n_bero` |
| 152 | Majors - 2nd Pl. | `tou_08` | `n_bero` |
| 153 | Majors - 1st Pl. | `tou_08` | `n_bero` |
| 154 | Lobby Poster | `tou_02` | `n_bero_4` |
| 155 | Unlocking the Door | `tou_06` | `n_bero` |
| 156 | Flattened | `tou_12` | `w_bero` |
| 157 | 1st Match with Rawk Hawk | `tou_08` | `dokan` |
| 158 | A New Champion | `tou_08` | `` |
| 158 | Champion's Room | `tou_07` | `n_bero` |
| 159 | Air Duct Entrance | `tou_07` | `n_bero` |
| 160 | Air Duct (1st Time) | `tou_13` | `e_bero_` |
| 161 | Eavesdropping | `tou_13` | `e_bero_` |
| 162 | Air Duct Exit | `tou_13` | `e_bero_` |
| 163 | Grubba's Plans | `tou_05` | `w_bero` |
| 164 | Boss Battle | `tou_03` | `w_bero` |
| 165 | Peach: The Secret Weapon | `aji_10` | `` |
| 166 | Peach: TEC's Request | `aji_17` | `w_bero` |
| 167 | Peach: Incognito | `aji_09` | `s_bero` |
| 168 | Peach: Grodus | `aji_10` | `w_bero` |
| 169 | Peach: Back to TEC | `aji_17` | `w_bero` |
| 170 | Bowser: The Great Tree | `mri_01` | `` |
| 171 | Bowser: Treasure? | `mri_01` | `player` |
| 171 | Bowser: Puni Elder | `mri_01` | `event` |
| 172 | Return to Rogueport | `tou_02` | `after_peach` |
| 173 | A Mail from Peach | `gor_03` | `n_bero` |
| 174 | Thousand-Year Door | `tik_05` | `e_bero` |
| 175 | Frankly's House Stg.3 | `gor_02` | `` |
| 176 | Darkly | `gor_02` | `w_bero` |
| 177 | To Stage 4 | `tik_07` | `e_bero` |
| 178 | Welcome to Stage 4 | `sys_01` | `stg_4` |
| 179 | Gatekeeper Conversation | `usu_01` | `w_bero` |
| 180 | The Mayor's a Pig! | `usu_00` | `e_bero` |
| 181 | Dinge | `usu_01` | `w_bero` |
| 182 | The Gatekeeper's a Pig! | `usu_01` | `w_bero` |
| 183 | Opening the Gate | `usu_01` | `w_bero` |
| 184 | Shop Key | `gra_02` | `w_bero_1` |
| 185 | Storage Room Unlocked | `usu_01` | `e_bero` |
| 187 | Paper Mage (Tube Mod) | `usu_01` | `e_bero` |
| 188 | Straw Tepee | `gra_02` | `w_bero_1` |
| 189 | Tree Trunk | `gra_04` | `e_bero` |
| 190 | Blow the Floor | `gra_05` | `w_bero` |
| 191 | Through the Hole | `gra_05` | `w_bero` |
| 192 | Trick Rock | `gra_05` | `w_bero` |
| 193 | Steeple Demo (EXT.) | `gra_06` | `sw_bero` |
| 194 | Steeple Demo (INT.) | `jin_00` | `w_bero` |
| 195 | Push the Statue | `jin_00` | `w_bero` |
| 196 | Boo Box | `jin_07` | `e_bero` |
| 197 | 1000 Boos | `jin_00` | `ana` |
| 198 | Key | `jin_00` | `e_bero_3` |
| 199 | Lock | `jin_00` | `e_bero_1` |
| 200 | Doopliss Battle | `jin_04` | `s_bero` |
| 201 | Trading Places | `jin_04` | `` |
| 202 | Superbombbomb Lost | `usu_00` | `evt_majo3` |
| 203 | Waiting Doopliss | `gra_00` | `e_bero` |
| 204 | Vivian | `usu_00` | `e_bero` |
| 205 | Superbombbomb Found | `usu_00` | `e_bero` |
| 206 | Vivian Joins | `usu_00` | `e_bero` |
| 207 | Waiting Doopliss 2 | `gra_00` | `w_bero` |
| 208 | Breaking the Floor | `jin_11` | `s_bero` |
| 209 | The Letter p | `jin_08` | `e_bero_2` |
| 210 | Name Guessing | `gra_00` | `e_bero` |
| 211 | Doopliss Battle 2 | `jin_04` | `s_bero` |
| 212 | Back to Normal | `jin_04` | `` |
| 213 | The Ruby Star | `jin_04` | `s_bero` |
| 214 | Shadow Sirens & Doopliss | `usu_00` | `s_bero` |
| 215 | Peach: X-Naut PhD Report | `aji_10` | `` |
| 215 | Peach: TEC's Quiz | `aji_17` | `w_bero` |
| 216 | Bowser: Blimp Area | `gor_04` | `` |
| 216 | Bowser: Flying | `tou_00` | `` |
| 217 | Bowser: Action Stage | `kpa_03` | `` |
| 218 | Bowser: Rogueport Dock | `gor_00` | `` |
| 219 | Leaving Twilight Town | `usu_00` | `` |
| 220 | A Mail from Peach | `tik_07` | `n_bero` |
| 221 | Thousand-Year Door | `tik_05` | `e_bero` |
| 222 | Frankly's House Stg.4 | `gor_02` | `` |
| 223 | Chatting with Flavio | `gor_01` | `e_bero` |
| 224 | Meet Bobbery | `gor_00` | `n_bero` |
| 225 | Bobbery Declines | `gor_02` | `w_bero` |
| 226 | Advice from Podley | `gor_01` | `e_bero` |
| 227 | Bobbery's Decision | `gor_02` | `w_bero` |
| 228 | To the Port | `gor_02` | `w_bero` |
| 229 | Off to the Keys | `gor_00` | `n_bero` |
| 230 | Logbook | `sys_01` | `stg_5` |
| 231 | Haunted | `muj_20` | `` |
| 232 | Deserted Island | `muj_00` | `` |
| 233 | Flavio & Pa-Patch | `muj_01` | `w_bero` |
| 233 | Flavio's Favor | `muj_01` | `` |
| 234 | Bobbery & the Bridge | `muj_04` | `w_bero` |
| 235 | Runaway Sailors | `muj_03` | `e_bero` |
| 235 | Flavio's Rescue Plan | `muj_01` | `e_bero1` |
| 235 | Saving Bobbery | `muj_05` | `w_bero` |
| 236 | Flavio's Wine | `muj_01` | `e_bero1` |
| 237 | Wine Obtained | `muj_01` | `e_bero1` |
| 238 | Bobbery Rescue 2 | `muj_05` | `w_bero` |
| 239 | Bobbery Joins | `muj_05` | `w_bero` |
| 240 | Flavio's Favor 2 | `muj_01` | `e_bero1` |
| 241 | Marco's Jewel | `muj_05` | `w_bero` |
| 242 | Gems and Jingles | `muj_05` | `w_bero` |
| 242 | The Skull Rock | `muj_05` | `w_bero` |
| 242 | Skull Rock Blast | `muj_05` | `w_bero` |
| 243 | Entering the Grotto | `dou_00` | `w_bero` |
| 244 | The Call of Cortez | `dou_01` | `w_bero` |
| 244 | Spikes (Floor) | `dou_02` | `w_bero_1` |
| 245 | The Blue Block | `dou_05` | `w_bero_1` |
| 246 | Grotto Key | `dou_04` | `e_bero` |
| 246 | Spikes (Wall) | `dou_10` | `n_bero` |
| 246 | Ship Hole | `dou_09` | `e_bero_2` |
| 246 | Paper Mage 4 | `dou_07` | `s_bero` |
| 247 | Boat Mod Obtained | `dou_07` | `s_bero` |
| 248 | Floodgate Handle | `dou_02` | `e_bero_1` |
| 248 | Floodgate | `dou_03` | `w_bero_2` |
| 249 | Wave-dodging | `dou_10` | `w_bero_1` |
| 250 | Shipwrecked Sailors | `dou_11` | `w_bero` |
| 250 | Switch Test | `dou_11` | `e_bero` |
| 250 | Thankful Sailors | `dou_11` | `w_bero` |
| 251 | Four-Eyes | `muj_10` | `w_bero` |
| 252 | Cortez's Warning | `muj_11` | `w_bero` |
| 253 | Cortez and the Treasure | `muj_12` | `w_bero` |
| 254 | Kicked Off | `muj_10` | `` |
| 255 | Escape Route | `dou_11` | `e_bero` |
| 256 | Hole in the Wall | `dou_11` | `e_bero` |
| 257 | True Identity | `muj_00` | `n_bero_02` |
| 258 | Return to the Grotto | `muj_00` | `e_bero` |
| 258 | Flavio Makes a Deal | `muj_12` | `w_bero` |
| 259 | All Aboard | `muj_10` | `A_b_bero03` |
| 260 | Pirates vs. X-Nauts | `muj_00` | `` |
| 261 | X-Nauts Retreat | `muj_00` | `` |
| 262 | Peach: TEC's Request 2 | `aji_10` | `` |
| 263 | Peach: Potion Puzzle | `aji_06` | `s_bero` |
| 264 | Peach: Disk Search | `aji_11` | `w_bero` |
| 265 | Peach: TEC Talk | `aji_17` | `` |
| 266 | Bowser: Twilight Town | `usu_00` | `` |
| 267 | Bowser: Twilight Town 2 | `usu_00` | `player` |
| 267 | Bowser: Bowser vs. X-Nauts | `usu_00` | `event` |
| 268 | Fair Winds! | `muj_00` | `` |
| 269 | Rogueport Dock | `gor_00` | `` |
| 270 | A Mail from Peach | `gor_00` | `` |
| 271 | Return to Keelhaul | `gor_00` | `n_bero` |
| 271 | Thousand-Year Door | `tik_05` | `e_bero` |
| 272 | Frankly's House Stg.5 | `gor_02` | `` |
| 273 | An Ill Don Pianta | `gor_03` | `` |
| 274 | Keelhaul Anytime | `muj_00` | `` |
| 275 | Lost Wedding Ring | `muj_02` | `w_bero` |
| 276 | Wedding Ring Delivery | `muj_02` | `w_bero` |
| 277 | F & F Sail Off | `muj_00` | `e_bero` |
| 278 | F & F Arrive | `gor_00` | `` |
| 279 | Train Ticket | `gor_03` | `` |
| 280 | Beldam Finds Out | `gor_03` | `` |
| 281 | The Train Leaves | `gor_04` | `s_bero` |
| 282 | Start | `sys_01` | `stg_6` |
| 283 | The Conductor | `rsh_04_a` | `e_bero` |
| 284 | A Case of Lost Stew | `rsh_03_a` | `w_bero` |
| 285 | Stained Carpet | `rsh_03_a` | `e_bero` |
| 286 | Grilling Heff T. | `rsh_02_a` | `e_bero` |
| 287 | Galley Kettle Discovered | `rsh_02_a` | `e_bero` |
| 288 | Pennington's Assistant | `rsh_04_a` | `e_bero` |
| 289 | Sylvia | `rsh_04_b` | `e_bero` |
| 290 | Bub | `rsh_04_b` | `e_bero` |
| 291 | Bub's Request | `rsh_04_b` | `e_bero` |
| 292 | The Conductor/Zip Toad | `rsh_04_b` | `e_bero` |
| 293 | Obtain Autograph | `rsh_00_b` | `w_bero` |
| 294 | Give Autograph | `rsh_04_b` | `e_bero` |
| 295 | Talk to the Conductor | `rsh_04_c` | `e_bero` |
| 296 | Ghost T. | `rsh_02_c` | `w_bero` |
| 297 | Ghost Request | `rsh_02_c` | `w_bero` |
| 298 | The Baggage Car | `rsh_04_c` | `e_bero` |
| 299 | Ghost Diary | `rsh_05_a` | `e_bero` |
| 300 | Blanket Exchange | `rsh_02_c` | `w_bero` |
| 301 | Give Blanket | `rsh_04_c` | `e_bero` |
| 302 | End of Day 1 | `rsh_02_c` | `w_bero` |
| 303 | Day 2 | `rsh_02_a` | `w_bero` |
| 304 | Document | `rsh_04_a` | `e_bero` |
| 305 | Vital Paper | `rsh_01_a` | `w_bero` |
| 306 | A Vital Clue | `rsh_04_a` | `e_bero` |
| 307 | Another Clue | `rsh_02_a` | `w_bero` |
| 308 | Zip Toad Appears | `rsh_02_a` | `w_bero` |
| 309 | Zip Toad Caught | `rsh_02_a` | `w_bero` |
| 310 | Riverside Station | `hom_00` | `hom_touchaku` |
| 311 | Station Key Obtained | `hom_00` | `n_bero_1` |
| 312 | Station Door Unlocked | `hom_00` | `n_bero_1` |
| 313 | Origami Stairs | `eki_01` | `w_dero` |
| 314 | Key | `eki_02` | `s_bero` |
| 315 | Unlocking the Door | `eki_01` | `w_dero` |
| 316 | Blow the Poster | `eki_03` | `w_bero_1` |
| 317 | 3 Blue Blocks | `eki_06` | `e_bero_1` |
| 318 | Origami Stairs | `eki_06` | `e_bero_1` |
| 319 | Spring Jump | `eki_05` | `w_bero_1` |
| 320 | Elevator Key | `eki_05` | `n_bero` |
| 321 | Ride the Elevator | `eki_00` | `e_bero` |
| 322 | Smorg (1st Encounter) | `eki_00` | `e_bero` |
| 323 | Swatting Smorgs | `eki_00` | `e_bero` |
| 324 | Origami Stairs | `eki_00` | `e_bero` |
| 325 | Drawbridge Down | `eki_00` | `e_bero` |
| 326 | Conductor Appears | `hom_00` | `n_bero_2` |
| 327 | End of Day 2 | `rsh_02_c` | `w_bero` |
| 328 | Day 3 Starts | `rsh_02_a` | `w_bero` |
| 329 | Engineer | `rsh_00_a` | `w_bero` |
| 330 | Baggage Car Smorgs | `rsh_05_a` | `e_bero` |
| 329 | Engineer | `rsh_00_a` | `w_bero` |
| 330 | Baggage Car Smorgs | `rsh_05_a` | `e_bero` |
| 331 | Escaping the Smorgs | `rsh_05_a` | `e_bero` |
| 332 | Smorg Miasma | `rsh_06_a` | `w_bero` |
| 334 | Poshley Heights | `rsh_01_a` | `w_bero` |
| 335 | The Sanctum Manager | `pik_01` | `nw_bero` |
| 336 | 3 Surprise Guests | `pik_02` | `s_bero` |
| 337 | The Hidden Pipe | `pik_02` | `s_bero` |
| 338 | The Real Garnet Star | `pik_03` | `s_bero` |
| 339 | Welcome Back | `pik_02` | `h_bero` |
| 340 | Peach: Grodus & X-Naut | `aji_10` | `` |
| 341 | Peach: TEC Deleted | `aji_17` | `w_bero` |
| 342 | Bowser: Rogueport | `gor_01` | `` |
| 343 | Bowser: Action Stage | `kpa_05` | `` |
| 344 | Bowser: Rawk Hawk | `kpa_07` | `` |
| 345 | Rogueport Station | `gor_04` | `resha_return` |
| 346 | A Mail from Peach | `gor_04` | `n_bero` |
| 347 | Thousand-Year Door | `tik_05` | `e_bero` |
| 348 | Frankly's House Stg.6 | `gor_02` | `` |
| 350 | 3 Minutes Later | `gor_02` | `w_bero` |
| 350 | A Way to the Moon | `gor_02` | `w_bero` |
| 351 | Ultra Hammer | `gor_01` | `e_bero` |
| 351 | Stone Block Smash | `tik_07` | `e_bero` |
| 351 | To Fahr Outpost | `tik_07` | `e_bero` |
| 352 | Start | `sys_01` | `stg_7` |
| 353 | Fahr Outpost (1st Visit) | `bom_01` | `w_bero` |
| 354 | Mayor Bob | `bom_02` | `w_bero` |
| 355 | Goldbob | `pik_00` | `se_bero` |
| 355 | Where's White?(Petalburg) | `nok_00` | `w_bero` |
| 355 | Where's White?(Keelhaul) | `muj_01` | `w_bero` |
| 355 | Where's White?(Glitzville) | `tou_01` | `n_bero` |
| 355 | Where's White?(Great Tree) | `mri_01` | `w_bero` |
| 355 | Where's White?(Twilight) | `usu_00` | `e_bero` |
| 355 | Gen. White Awakens | `bom_02` | `w_bero` |
| 356 | Back Online | `bom_02` | `w_bero` |
| 357 | The Cannon | `bom_01` | `e_bero` |
| 358 | To the Moon | `moo_00` | `` |
| 359 | A Pipe Appears | `moo_02` | `w_bero` |
| 360 | Inside the Building | `aji_19` | `w_bero` |
| 361 | Elite X-Nauts | `aji_00` | `w_bero` |
| 362 | Elevator Key A(Lit Floor) | `aji_02` | `w_bero` |
| 363 | Elevator Activated | `aji_01` | `e_bero_1` |
| 364 | Password for Today | `aji_09` | `s_bero` |
| 365 | Password Entry | `aji_01` | `w_bero_2` |
| 366 | Quiz Cleared | `aji_04` | `w_bero` |
| 367 | Elevator Key B | `aji_04` | `w_bero` |
| 368 | Elevator Activated 2 | `aji_01` | `n_bero_4` |
| 368 | Room Key A | `aji_05` | `e_bero` |
| 368 | Room Key B | `aji_12` | `e_bero` |
| 368 | Room Key C | `aji_10` | `w_bero` |
| 369 | Factory Door | `aji_18` | `w_bero` |
| 370 | Conveyor Belt | `aji_13` | `w_bero` |
| 371 | Off-screen Stairs | `aji_13` | `w_bero` |
| 372 | The Door to Lord Crump | `aji_13` | `w_bero` |
| 373 | Lord Crump Defeated | `aji_14` | `w_bero` |
| 374 | Bowser: Poshley Heights | `pik_01` | `` |
| 375 | Bowser: Poshley Sanctum | `pik_01` | `` |
| 375 | Bowser: Crystal Star | `pik_02` | `` |
| 376 | The Last Mail | `aji_18` | `e_bero` |
| 377 | The Hideout Explodes | `aji_07` | `s_bero` |
| 378 | A Waiting Prof. Frankly  | `tik_00` | `` |
| 379 | Thousand-Year Door | `tik_05` | `e_bero` |
| 380 | The Pedestal | `tik_05` | `e_bero` |
| 381 | To the Last Dungeon | `tik_05` | `e_bero` |
| 382 | Start | `sys_01` | `stg_8` |
| 383 | 1000 Dry Bones | `las_05` | `w_bero` |
| 384 | Key | `las_05` | `w_bero` |
| 385 | Lock | `las_05` | `w_bero` |
| 386 | Follow the Lit Torches | `las_08` | `w_bero_1` |
| 387 | The Palace Garden | `las_09` | `w_bero` |
| 388 | Gloomtail | `las_26` | `w_bero` |
| 389 | Star Key Slot | `las_10` | `s_bero` |
| 390 | Moving Planets | `las_10` | `tenkyugi_evt` |
| 391 | Beldam Confrontation | `las_09` | `majyorin_evt` |
| 392 | The New Path | `las_19` | `w_bero` |
| 393 | Key | `las_22` | `s_bero` |
| 394 | Lock | `las_22` | `s_bero` |
| 395 | Star Puzzle | `las_20` | `e_bero` |
| 396 | Large Stone Block | `las_24` | `w_bero` |
| 397 | Key | `las_24` | `s_bero_2` |
| 398 | Lock | `las_25` | `w_bero` |
| 399 | Queen's Chamber | `las_28` | `w_bero` |
| 400 | Grodus | `las_28` | `w_bero` |
| 400 | Bowser | `las_28` | `koopa_evt` |
| 401 | The Return of the Queen | `las_29` | `w_bero` |
| 401 | End of the World 1 | `gor_01` | `sekai_yami1` |
| 401 | The Shadow Queen | `las_29` | `sekai_yami1` |
| 401 | End of the World 2 | `usu_00` | `sekai_yami2` |
| 401 | Shadow Peach | `las_29` | `sekai_yami2` |
| 401 | The Crystal Stars | `las_29` | `starstone` |
| 401 | Words of Support 1 | `gor_01` | `minnnanokoe` |
| 401 | Words of Support 2 | `usu_00` | `minnnanokoe` |
| 401 | Words of Support 3 | `las_29` | `minnnanokoe` |
| 402 | After the Battle | `las_29` | `owari` |
| 403 | Epilogue | `gor_11` | `` |
| 403 | Rogueport Dock | `gor_00` | `` |
| 403 | Sail Away | `muj_21` | `` |
| 403 | Mario's House | `aaa_00` | `` |
| 403 | Professor Frankly | `gor_02` | `` |
| 403 | Goombella | `hei_00` | `` |
| 403 | Koops | `nok_01` | `` |
| 403 | Mini-Yoshi | `tou_08` | `` |
| 403 | Vivian | `usu_00` | `` |
| 403 | Bobbery | `muj_20` | `` |
| 403 | Ms. Mowz | `gor_01` | `` |
| 403 | X-Nauts | `pik_04` | `` |
| 403 | Moon | `tik_00` | `` |
| 403 | Goombella 2 | `gor_00` | `epilogue2` |
| 403 | Mario's House 2 | `aaa_00` | `epilogue2` |
| 404 | End Credits | `end_00` | `` |
| 405 | Return to Rogueport | `gor_00` | `` |
| 406 | Rogueport | `gor_00` | `n_bero` |
