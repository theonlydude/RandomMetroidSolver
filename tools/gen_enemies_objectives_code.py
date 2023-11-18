#!/usr/bin/python3

import sys, os, re, json

nameRegex = re.compile(r'[^a-z0-9]')

with open("enemies_objectives_data.json", "r") as fp:
    nmyObjData = json.load(fp)

with open("patches/common/src/include/enemies_events.asm", "w") as fp:
    fp.write("include\n\n")
    for nmyType, nmyData in nmyObjData.items():
        nmyName = nameRegex.sub('_', nmyType.lower())
        fp.write("!%s_all_event #= !enemies_event_base+%d\n\n" % (nmyName, nmyData['event']))        
        for _, areaData in nmyData["areas"].items():
            for room, event in areaData["room_events"].items():
                roomName = nameRegex.sub('_', room.lower())
                fp.write("!%s_%s_all_event #= !enemies_event_base+%d\n" % (nmyName, roomName, event))
            fp.write("\n")
            for room, enemies in areaData["enemies"].items():
                roomName = nameRegex.sub('_', room.lower())
                for i, nmy in enumerate(enemies):
                    fp.write("!%s_%s_%d_event #= !enemies_event_base+%d\n" % (nmyName, roomName, i, nmy["event"]))
                fp.write("\n")
            fp.write("\n")

with open("patches/common/src/objectives/enemies.asm", "w") as fp:
    fp.write("include\n\nenemies_table:\n")
    idx = 0
    for nmyType, nmyData in nmyObjData.items():
        nmyName = nameRegex.sub('_', nmyType.lower())
        for _, areaData in nmyData["areas"].items():
            for room, enemies in areaData["enemies"].items():
                roomName = nameRegex.sub('_', room.lower())
                for i, nmy in enumerate(enemies):
                    fp.write(f"\tdw !{nmyName}_{roomName}_{i}_event, {nmyName}_type, {nmyName}_{roomName}_events, 0\n")
                    fp.write("pushpc\n")
                    fp.write("org $%06x\n" % nmy['props_snes_addr'])
                    fp.write("\tdw $%04x\n" % (nmy['props'] | 0x4000 | (idx << 3)))
                    fp.write("pullpc\n")
                    idx += 1
    fp.write("\n")
    typeIdx = 0
    for nmyType, nmyData in nmyObjData.items():
        nmyName = nameRegex.sub('_', nmyType.lower())
        fp.write(f"%export({nmyName}_type)\n")
        fp.write("\tdb $00 ; to be filled by randomizer\n")
        fp.write("\tdw $%02x\n" % typeIdx)
        fp.write(f"\tdw !{nmyName}_all_event\n")
        fp.write("\n")
        for _, areaData in nmyData["areas"].items():
            for room, enemies in areaData["enemies"].items():
                roomName = nameRegex.sub('_', room.lower())
                fp.write(f"{nmyName}_{roomName}_events:\n")
                fp.write(f"\tdw {2*(len(enemies)+1)}\n\n")
                for i in range(len(enemies)):
                    fp.write(f"\tdw !{nmyName}_{roomName}_{i}_event\n")
                fp.write(f"\n\tdw !{nmyName}_{roomName}_all_event\n\n")
        typeIdx += 1
