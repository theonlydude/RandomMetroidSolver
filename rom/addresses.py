from rom.rom import snes_to_pc, pc_to_snes

# TODO::add patches

class Byte(object):
    def __init__(self, value):
        self.value = value

    def expand(self):
        return [self.value]

class Word(object):
    def __init__(self, value):
        self.value = value

    def expand(self):
        return [self.value, self.value+1]

class Long(object):
    def __init__(self, value):
        self.value = value

    def expand(self):
        return [self.value, self.value+1, self.value+2]

class ValueSingle(object):
    def __init__(self, value, storage=Word):
        self.value = snes_to_pc(value)
        self.storage = storage

    def getOne(self):
        return self.value

    def getAll(self):
        return [self.value]

    def getWeb(self):
        return self.storage(self.value).expand()

class ValueList(object):
    def __init__(self, values, storage=Word):
        self.values = [snes_to_pc(value) for value in values]
        self.storage = storage

    def getOne(self):
        return self.values[0]

    def getAll(self):
        return self.values

    def getWeb(self):
        out = []
        for value in self.values:
            out += self.storage(value).expand()
        return out

class ValueRange(object):
    def __init__(self, start, length=-1, end=-1):
        self.start = snes_to_pc(start)
        if length != -1:
            self.end = self.start + length
            self.length = length
        else:
            self.end = snes_to_pc(end)
            self.length = self.end - self.start

    def getOne(self):
        return self.start

    def getAll(self):
        return [self.start+i for i in range(self.length)]

    def getWeb(self):
        return [self.start, self.end]

class Addresses(object):
    @staticmethod
    def getOne(key):
        value = Addresses.addresses[key]
        return value.getOne()

    @staticmethod
    def getAll(key):
        value = Addresses.addresses[key]
        return value.getAll()

    @staticmethod
    def getWeb(key):
        value = Addresses.addresses[key]
        return value.getWeb()

    @staticmethod
    def getRange(key):
        value = Addresses.addresses[key]
        return value.getWeb()

    addresses = {
        'totalItems': ValueList([0x8BE656, 0x8BE6B3], storage=Byte),
        'totalItemsPercent': ValueList([0xA1FC72, 0xA1FC7A, 0xA1FC82, 0xA1FC8A]),

        'objectivesList': ValueSingle(0xA1FA80),
        'objectivesSpritesOAM': ValueSingle(0x82FE83),
        'objectivesText': ValueSingle(0xB6F200),
        # individual objectives function addresses
        'objective[kraid_is_dead]': ValueSingle(0xA1FB90),
        'objective[phantoon_is_dead]': ValueSingle(0xA1FB98),
        'objective[draygon_is_dead]': ValueSingle(0xA1FBA0),
        'objective[ridley_is_dead]': ValueSingle(0xA1FBA8),
        'objective[all_g4_dead]': ValueSingle(0xA1FBB0),
        'objective[spore_spawn_is_dead]': ValueSingle(0xA1FBC6),
        'objective[botwoon_is_dead]': ValueSingle(0xA1FBCE),
        'objective[crocomire_is_dead]': ValueSingle(0xA1FBD6),
        'objective[golden_torizo_is_dead]': ValueSingle(0xA1FBDE),
        'objective[all_mini_bosses_dead]': ValueSingle(0xA1FBE6),
        'objective[scavenger_hunt_completed]': ValueSingle(0xA1FBFC),
        'objective[boss_1_killed]': ValueSingle(0xA1FC3C),
        'objective[boss_2_killed]': ValueSingle(0xA1FC45),
        'objective[boss_3_killed]': ValueSingle(0xA1FC4E),
        'objective[miniboss_1_killed]': ValueSingle(0xA1FC57),
        'objective[miniboss_2_killed]': ValueSingle(0xA1FC60),
        'objective[miniboss_3_killed]': ValueSingle(0xA1FC69),
        'objective[collect_25_items]': ValueSingle(0xA1FC72),
        'objective[collect_50_items]': ValueSingle(0xA1FC7A),
        'objective[collect_75_items]': ValueSingle(0xA1FC82),
        'objective[collect_100_items]': ValueSingle(0xA1FC8A),
        'objective[nothing_objective]': ValueSingle(0xA1FC92),
        'objective[fish_tickled]': ValueSingle(0xA1FCBA),
        'objective[orange_geemer]': ValueSingle(0xA1FCC2),
        'objective[shak_dead]': ValueSingle(0xA1FCCA),
        'objective[all_major_items]': ValueSingle(0xA1FCD6),
        'objective[crateria_cleared]': ValueSingle(0xA1FCED),
        'objective[green_brin_cleared]': ValueSingle(0xA1FCF5),
        'objective[red_brin_cleared]': ValueSingle(0xA1FCFD),
        'objective[ws_cleared]': ValueSingle(0xA1FD05),
        'objective[kraid_cleared]': ValueSingle(0xA1FD0D),
        'objective[upper_norfair_cleared]': ValueSingle(0xA1FD15),
        'objective[croc_cleared]': ValueSingle(0xA1FD1D),
        'objective[lower_norfair_cleared]': ValueSingle(0xA1FD25),
        'objective[west_maridia_cleared]': ValueSingle(0xA1FD2D),
        'objective[east_maridia_cleared]': ValueSingle(0xA1FD35),
        'objective[all_chozo_robots]': ValueSingle(0xA1FD3D),
        'objective[visited_animals]': ValueSingle(0xA1FD5C),

        'majorsSplit': ValueSingle(0x82fb6c, storage=Byte),
        # scavenger hunt items list (17 prog items (including ridley) + hunt over + terminator, each is a word)
        'scavengerOrder': ValueRange(0xA1F5D8, length=(17+1+1)*2),
        'plandoAddresses': ValueRange(0xdee000, length=128),
        'plandoTransitions': ValueSingle(0xdee100),
        'escapeTimer': ValueSingle(0x809e21),
        'escapeTimerTable': ValueSingle(0xA1F0AA),
        'startAP': ValueSingle(0xa1f200),
        'customDoorsAsm': ValueSingle(0x8ff800),
        'locIdsByArea': ValueRange(0xA1F568, end=0xA1F5D7),
        'plmSpawnTable': ValueSingle(0x8fe9a0),
        'plmSpawnRoomTable': ValueSingle(0x8ff000),
        'moonwalk': ValueSingle(0x81b35d),
        'additionalETanks': ValueSingle(0xA1F470),
        'hellrunRate': ValueSingle(0x8DE387),
        'itemsMask': ValueSingle(0x82FAD9),
        'beamsMask': ValueSingle(0x82FADB),
        'BTtweaksHack1': ValueSingle(0x84ba6f+3),
        'BTtweaksHack2': ValueSingle(0x84d33b+3)
    }
