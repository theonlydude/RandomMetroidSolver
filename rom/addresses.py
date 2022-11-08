from rom.addressTypes import ValueList, ValueSingle, ValueRange, Byte, Word, Long
from rom.objectivesAddresses import objectivesAddr

# TODO::add patches


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

    @staticmethod
    def updateFromSymbols(symbols):
        addrs = Addresses.addresses
        addrs.update({sym:ValueSingle(symbols.getAddress(sym)) for sym in symbols.getAbsoluteSymbols()})
        # for more readable names and complex values:
        addrs.update({
            'totalItems': ValueSingle(symbols.getAddress('endingtotals', 'total_items'), storage=Byte),
            'majorsSplit': ValueSingle(symbols.getAddress('seed_display', 'InfoStr'), storage=Byte),
            # scavenger hunt items list (17 prog items (including ridley) + hunt over + terminator, each is a word)
            'scavengerOrder': ValueRange(symbols.getAddress('varia_hud', 'scav_order'), length=(17+1+1)*2),
            'escapeTimer': ValueSingle(symbols.getAddress('rando_escape', 'timer_value')),
            'escapeTimerTable': ValueSingle(symbols.getAddress('rando_escape', 'timer_values_by_area_id')),
            'startAP': ValueSingle(symbols.getAddress('new_game', 'start_location')),
            'customDoorsAsm': ValueRange(symbols.getAddress('door_transition', 'generated_door_asm'),
                                         end=symbols.getAddress('door_transition', 'generated_door_asm_end')),
            'locIdsByArea': ValueRange(symbols.getAddress('varia_hud', 'locs_start'),
                                       end=symbols.getAddress('varia_hud', 'locs_end')),
            'plmSpawnTable': ValueSingle(symbols.getAddress('plm_spawn', 'plm_lists')),
            'plmSpawnRoomTable': ValueSingle(symbols.getAddress('plm_spawn', 'room_plms_upwards')),
            'additionalETanks': ValueSingle(symbols.getAddress('new_game', 'additional_etanks'), storage=Byte),
            'BTtweaksHack1': ValueSingle(symbols.getAddress('bomb_torizo', 'bt_grey_door_instr_nops')),
            'BTtweaksHack2': ValueSingle(symbols.getAddress('bomb_torizo', 'bt_instr_nops')),
            'introText': ValueSingle(symbols.getAddress('intro_text', 'page1_text'))
        })

    addresses = {
        'plandoAddresses': ValueRange(0xdee000, length=128),
        'plandoTransitions': ValueSingle(0xdee100),
        'moonwalk': ValueSingle(0x81b35d),
        'hellrunRate': ValueSingle(0x8DE387)
    }

Addresses.addresses.update(objectivesAddr)
