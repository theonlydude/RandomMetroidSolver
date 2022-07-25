from rom.addressTypes import ValueList, ValueSingle
# generated from asar output
# A1 start: A1FA80
objectivesAddr = {
    # --- objectives checker functions: A1FA80 ---
    'objectivesList': ValueSingle(0xA1FA80),
    'objective[kraid_is_dead]': ValueSingle(0xA1FBAE),
    'objective[phantoon_is_dead]': ValueSingle(0xA1FBB6),
    'objective[draygon_is_dead]': ValueSingle(0xA1FBBE),
    'objective[ridley_is_dead]': ValueSingle(0xA1FBC6),
    'objective[all_g4_dead]': ValueSingle(0xA1FBCE),
    'objective[spore_spawn_is_dead]': ValueSingle(0xA1FBE4),
    'objective[botwoon_is_dead]': ValueSingle(0xA1FBEC),
    'objective[crocomire_is_dead]': ValueSingle(0xA1FBF4),
    'objective[golden_torizo_is_dead]': ValueSingle(0xA1FBFC),
    'objective[all_mini_bosses_dead]': ValueSingle(0xA1FC04),
    'objective[scavenger_hunt_completed]': ValueSingle(0xA1FC1A),
    'objective[boss_1_killed]': ValueSingle(0xA1FC5A),
    'objective[boss_2_killed]': ValueSingle(0xA1FC63),
    'objective[boss_3_killed]': ValueSingle(0xA1FC6C),
    'objective[miniboss_1_killed]': ValueSingle(0xA1FC75),
    'objective[miniboss_2_killed]': ValueSingle(0xA1FC7E),
    'objective[miniboss_3_killed]': ValueSingle(0xA1FC87),
    'objective[collect_25_items]': ValueSingle(0xA1FC90),
    '__pct25': 0xA1FC94,
    'objective[collect_50_items]': ValueSingle(0xA1FC98),
    '__pct50': 0xA1FC9C,
    'objective[collect_75_items]': ValueSingle(0xA1FCA0),
    '__pct75': 0xA1FCA4,
    'objective[collect_100_items]': ValueSingle(0xA1FCA8),
    '__pct100': 0xA1FCAC,
    'objective[nothing_objective]': ValueSingle(0xA1FCB0),
    'objective[fish_tickled]': ValueSingle(0xA1FCD8),
    'objective[orange_geemer]': ValueSingle(0xA1FCE0),
    'objective[shak_dead]': ValueSingle(0xA1FCE8),
    'itemsMask': ValueSingle(0xA1FCF0),
    'beamsMask': ValueSingle(0xA1FCF2),
    'objective[all_major_items]': ValueSingle(0xA1FCF4),
    'objective[crateria_cleared]': ValueSingle(0xA1FD0B),
    'objective[green_brin_cleared]': ValueSingle(0xA1FD13),
    'objective[red_brin_cleared]': ValueSingle(0xA1FD1B),
    'objective[ws_cleared]': ValueSingle(0xA1FD23),
    'objective[kraid_cleared]': ValueSingle(0xA1FD2B),
    'objective[upper_norfair_cleared]': ValueSingle(0xA1FD33),
    'objective[croc_cleared]': ValueSingle(0xA1FD3B),
    'objective[lower_norfair_cleared]': ValueSingle(0xA1FD43),
    'objective[west_maridia_cleared]': ValueSingle(0xA1FD4B),
    'objective[east_maridia_cleared]': ValueSingle(0xA1FD53),
    'objective[all_chozo_robots]': ValueSingle(0xA1FD5B),
    'objective[visited_animals]': ValueSingle(0xA1FD7A),
    'objective[king_cac_dead]': ValueSingle(0xA1FDC6),
    # A1 end: A1FDCE
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
