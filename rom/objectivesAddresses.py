from rom.addressTypes import ValueList, ValueSingle
# generated from asar output
# A1 start: A1FA80
objectivesAddr = {
    # --- objectives checker functions: A1FA80 ---
    'objectivesList': ValueSingle(0xA1FA80),
    'objective[kraid_is_dead]': ValueSingle(0xA1FBB8),
    'objective[phantoon_is_dead]': ValueSingle(0xA1FBC0),
    'objective[draygon_is_dead]': ValueSingle(0xA1FBC8),
    'objective[ridley_is_dead]': ValueSingle(0xA1FBD0),
    'objective[all_g4_dead]': ValueSingle(0xA1FBD8),
    'objective[spore_spawn_is_dead]': ValueSingle(0xA1FBEE),
    'objective[botwoon_is_dead]': ValueSingle(0xA1FBF6),
    'objective[crocomire_is_dead]': ValueSingle(0xA1FBFE),
    'objective[golden_torizo_is_dead]': ValueSingle(0xA1FC06),
    'objective[all_mini_bosses_dead]': ValueSingle(0xA1FC0E),
    'objective[scavenger_hunt_completed]': ValueSingle(0xA1FC24),
    'objective[boss_1_killed]': ValueSingle(0xA1FC64),
    'objective[boss_2_killed]': ValueSingle(0xA1FC6D),
    'objective[boss_3_killed]': ValueSingle(0xA1FC76),
    'objective[miniboss_1_killed]': ValueSingle(0xA1FC7F),
    'objective[miniboss_2_killed]': ValueSingle(0xA1FC88),
    'objective[miniboss_3_killed]': ValueSingle(0xA1FC91),
    'objective[collect_25_items]': ValueSingle(0xA1FC9A),
    '__pct25': 0xA1FC9F,
    'objective[collect_50_items]': ValueSingle(0xA1FCA2),
    '__pct50': 0xA1FCA7,
    'objective[collect_75_items]': ValueSingle(0xA1FCAA),
    '__pct75': 0xA1FCAF,
    'objective[collect_100_items]': ValueSingle(0xA1FCB2),
    '__pct100': 0xA1FCB7,
    'objective[nothing_objective]': ValueSingle(0xA1FCBA),
    'objective[fish_tickled]': ValueSingle(0xA1FCE2),
    'objective[orange_geemer]': ValueSingle(0xA1FCEA),
    'objective[shak_dead]': ValueSingle(0xA1FCF2),
    'itemsMask': ValueSingle(0xA1FCFA),
    'beamsMask': ValueSingle(0xA1FCFC),
    'objective[all_major_items]': ValueSingle(0xA1FCFE),
    'objective[crateria_cleared]': ValueSingle(0xA1FD15),
    'objective[green_brin_cleared]': ValueSingle(0xA1FD1D),
    'objective[red_brin_cleared]': ValueSingle(0xA1FD25),
    'objective[ws_cleared]': ValueSingle(0xA1FD2D),
    'objective[kraid_cleared]': ValueSingle(0xA1FD35),
    'objective[upper_norfair_cleared]': ValueSingle(0xA1FD3D),
    'objective[croc_cleared]': ValueSingle(0xA1FD45),
    'objective[lower_norfair_cleared]': ValueSingle(0xA1FD4D),
    'objective[west_maridia_cleared]': ValueSingle(0xA1FD55),
    'objective[east_maridia_cleared]': ValueSingle(0xA1FD5D),
    'objective[all_chozo_robots]': ValueSingle(0xA1FD65),
    'objective[visited_animals]': ValueSingle(0xA1FD84),
    'objective[king_cac_dead]': ValueSingle(0xA1FDD0),
    # A1 end: A1FDD8
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
