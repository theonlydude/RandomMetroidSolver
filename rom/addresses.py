from rom.addressTypes import ValueList, ValueSingle, ValueRange, Byte, Word, Long

# TODO::add patches

MAX_OBJECTIVES = 18

class Addresses(object):
    # load symbol on the fly when needed
    @staticmethod
    def get(key):
        value = Addresses.addresses.get(key)
        if value is None:
            addr = Addresses.symbols.getAddress(key)
            if addr is not None:
                value = ValueSingle(addr)
                Addresses.addresses[key] = value
        if value is None:
            raise ValueError("Unknown address '%s'" % key)
        return value

    @staticmethod
    def getOne(key):
        value = Addresses.get(key)
        return value.getOne()

    @staticmethod
    def getAll(key):
        value = Addresses.get(key)
        return value.getAll()

    @staticmethod
    def getWeb(key):
        value = Addresses.get(key)
        return value.getWeb()

    @staticmethod
    def getRange(key):
        value = Addresses.get(key)
        return value.getWeb()

    @staticmethod
    def updateFromSymbols(symbols):
        Addresses.addresses = {
            'plandoAddresses': ValueRange(0xdee000, length=256),
            'plandoTransitions': ValueSingle(0xdee100),
            'moonwalk': ValueSingle(0x81b35d),
            'hellrunRate': ValueSingle(0x8DE387),
            'morphEyeAI': ValueSingle(0xa890e6),
            'morphHeadAI': ValueSingle(0xa8e8b2),
            'paletteShip_1': ValueSingle(0xA2A59E),
            'paletteShip_2': ValueSingle(0xA2A5BE),
            'paletteShip7_1': ValueSingle(0x8DD6BA),
            'paletteShip7_2': ValueSingle(0x8DD900),
            'paletteShipGlow_1': ValueSingle(0x8DCA4E),
            'paletteShipGlow_2': ValueSingle(0x8DCAAA),
            'westOceanScrollingSky': ValueSingle(0x8fb7bb),
            'versionOamListPtr1': ValueSingle(0x8ba0e3),
            'versionOamListPtr2': ValueSingle(0x8ba0e9),
            'versionOamList': ValueSingle(0x8CF3E9),
            'musicDataTable': ValueSingle(0x8FE7E4)
        }

        Addresses.symbols = symbols

        # for more readable names and complex values:
        Addresses.addresses.update({
            'totalItems': ValueSingle(symbols.getAddress('endingtotals', 'total_items'), storage=Byte),
            'majorsSplit': ValueSingle(symbols.getAddress('seed_display', 'InfoStr'), storage=Byte),
            # scavenger hunt items list (17 prog items (including ridley) + hunt over + terminator, each is a word)
            'scavengerOrder': ValueRange(symbols.getAddress('varia_hud', 'scav_order'), length=(17+1+1)*2),
            'escapeTimer': ValueSingle(symbols.getAddress('rando_escape_common', 'timer_value')),
            'escapeTimerTable': ValueSingle(symbols.getAddress('rando_escape_common', 'timer_values_by_area_id')),
            'startAP': ValueSingle(symbols.getAddress('start', 'start_location')),
            'customDoorsAsm': ValueRange(symbols.getAddress('door_transition', 'generated_door_asm'),
                                         end=symbols.getAddress('door_transition', 'generated_door_asm_end')),
            'locIdsByArea': ValueRange(symbols.getAddress('objectives', 'locs_start'),
                                       end=symbols.getAddress('objectives', 'locs_end')),
            'plmSpawnTable': ValueSingle(symbols.getAddress('plm_spawn', 'plm_lists')),
            'plmSpawnRoomTable': ValueSingle(symbols.getAddress('plm_spawn', 'room_plms_upwards')),
            'introText': ValueSingle(symbols.getAddress('intro_text', 'page1_text')),
            'objectivesList': ValueSingle(symbols.getAddress('objectives', 'objective_funcs')),
            'objectiveEventsArray': ValueRange(symbols.getAddress('objectives', 'objective_events'), length=2*MAX_OBJECTIVES),
            'itemsMask': ValueSingle(symbols.getAddress('objectives', 'all_items_mask')),
            'beamsMask': ValueSingle(symbols.getAddress('objectives', 'all_beams_mask')),
            'totalItemsPercent': ValueList([symbols.getAddress('objectives', 'collect_%d_items_pct' % pct) for pct in [25,50,75,100]])
        })

    addresses = {}
