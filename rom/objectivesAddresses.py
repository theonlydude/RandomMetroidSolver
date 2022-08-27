from rom.addressTypes import ValueList, ValueSingle, ValueRange
# generated from asar output
# A1 start: A1FA80
objectivesAddr = {
    # --- objectives checker functions: A1FA80 ---
    'objectivesList': ValueSingle(0xA1FA80),
    'objectiveEventsArray': ValueRange(0xA1FB1A, length=2*5),
    'objective[kraid_is_dead]': ValueSingle(0xA1FBC2),
    'objective[phantoon_is_dead]': ValueSingle(0xA1FBCA),
    'objective[draygon_is_dead]': ValueSingle(0xA1FBD2),
    'objective[ridley_is_dead]': ValueSingle(0xA1FBDA),
    'objective[all_g4_dead]': ValueSingle(0xA1FBE2),
    'objective[spore_spawn_is_dead]': ValueSingle(0xA1FBF8),
    'objective[botwoon_is_dead]': ValueSingle(0xA1FC00),
    'objective[crocomire_is_dead]': ValueSingle(0xA1FC08),
    'objective[golden_torizo_is_dead]': ValueSingle(0xA1FC10),
    'objective[all_mini_bosses_dead]': ValueSingle(0xA1FC18),
    'objective[scavenger_hunt_completed]': ValueSingle(0xA1FC2E),
    'objective[boss_1_killed]': ValueSingle(0xA1FC6E),
    'objective[boss_2_killed]': ValueSingle(0xA1FC77),
    'objective[boss_3_killed]': ValueSingle(0xA1FC80),
    'objective[miniboss_1_killed]': ValueSingle(0xA1FC89),
    'objective[miniboss_2_killed]': ValueSingle(0xA1FC92),
    'objective[miniboss_3_killed]': ValueSingle(0xA1FC9B),
    'objective[collect_25_items]': ValueSingle(0xA1FCA4),
    '__pct25': 0xA1FCA9,
    'objective[collect_50_items]': ValueSingle(0xA1FCAC),
    '__pct50': 0xA1FCB1,
    'objective[collect_75_items]': ValueSingle(0xA1FCB4),
    '__pct75': 0xA1FCB9,
    'objective[collect_100_items]': ValueSingle(0xA1FCBC),
    '__pct100': 0xA1FCC1,
    'objective[nothing_objective]': ValueSingle(0xA1FCC4),
    'objective[fish_tickled]': ValueSingle(0xA1FCEC),
    'objective[orange_geemer]': ValueSingle(0xA1FCF4),
    'objective[shak_dead]': ValueSingle(0xA1FCFC),
    'itemsMask': ValueSingle(0xA1FD04),
    'beamsMask': ValueSingle(0xA1FD06),
    'objective[all_major_items]': ValueSingle(0xA1FD08),
    'objective[crateria_cleared]': ValueSingle(0xA1FD1F),
    'objective[green_brin_cleared]': ValueSingle(0xA1FD27),
    'objective[red_brin_cleared]': ValueSingle(0xA1FD2F),
    'objective[ws_cleared]': ValueSingle(0xA1FD37),
    'objective[kraid_cleared]': ValueSingle(0xA1FD3F),
    'objective[upper_norfair_cleared]': ValueSingle(0xA1FD47),
    'objective[croc_cleared]': ValueSingle(0xA1FD4F),
    'objective[lower_norfair_cleared]': ValueSingle(0xA1FD57),
    'objective[west_maridia_cleared]': ValueSingle(0xA1FD5F),
    'objective[east_maridia_cleared]': ValueSingle(0xA1FD67),
    'objective[all_chozo_robots]': ValueSingle(0xA1FD6F),
    'objective[visited_animals]': ValueSingle(0xA1FD8E),
    'objective[king_cac_dead]': ValueSingle(0xA1FDDA),
    # A1 end: A1FDE2
    # Pause stuff: 82FB6D
    # *** completed spritemaps: 82FE83
    'objectivesSpritesOAM': ValueSingle(0x82FE83),
    # 82 end: 82FEB0
    'objectivesText': ValueSingle(0xB6F200),
}
_pctList = []
for pct in [25,50,75,100]:
    _pctList.append(objectivesAddr['__pct%d' % pct])
    del objectivesAddr['__pct%d' % pct]
objectivesAddr['totalItemsPercent'] = ValueList(_pctList)
