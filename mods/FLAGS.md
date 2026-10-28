# Known global flags

Select the flag index row and press A to cycle through known flags. Left/right still selects an arbitrary flag; press A on the value row to toggle it. Names describe observed uses, not complete story presets. Other values remain unknown.

| Flag | Observed meaning when set |
| --- | --- |
| 0 | Shop tutorial shown |
| 7 | Frankly email event triggered; also awards newsletter registration |
| 8 | Koopley email event triggered |
| 9 | Koopie Koo email event triggered |
| 10 | Petuni email event triggered |
| 11 | Boo email event triggered |
| 12 | Pa-Patch email event triggered |
| 13 | King K email event triggered |
| 14 | Zip Toad email event triggered |
| 15 | Rawk Hawk email event triggered |
| 16 | Ghost T email event triggered; also awards the final newsletter |
| 17 | Newsletter premiere event triggered |
| 18 | Newsletter issue 2 event triggered |
| 19 | Newsletter issue 3 event triggered |
| 20 | Newsletter issue 4 event triggered |
| 21 | Newsletter issue 5 event triggered |
| 22 | Newsletter issue 6 event triggered |
| 37 | First email received |
| 38 | An email has been read |
| 233 | Save block tutorial shown |
| 234 | Recovery block tutorial shown |
| 235 | Item tutorial shown |
| 1213 | Gus fight-related flag |
| 1240 | Arcade type 0 top-score condition |
| 1241 | Arcade type 3 top-score condition |
| 1242 | Arcade top-score condition for other types |
| 1243 | Arcade score-record condition |
| 1498 | Hooktail fight-related flag |
| 2226 | Atomic Boo fight-related flag |
| 2388 | Glitz Pit match reserved |
| 2443 | Previous Glitz Pit match won |

In the upstream source, tutorial and arcade behavior can be inspected in `src/event/evt_shop.c`, `src/event/evt_mobj.c`, `src/event/evt_sub.c`, and `rels/yuu/src/event/evt_yuuranking.c`. Fight and Glitz Pit associations were cross-checked against [TTYD Practice Codes](https://github.com/Zephiles/TTYD-Practice-Codes). A fight-related flag may have additional uses; clearing it alone does not guarantee a repeatable fight.

Mail-event flags record whether a delivery event has executed. Setting one does not add its mail to the mailbox; clearing one may allow the event to trigger again only when its other conditions are met. In the upstream source, the event-to-mail mapping is in `src/event/evt_sub.c` and `src/data/mail_data.c`.
