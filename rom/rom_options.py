
from rom.rom import snes_to_pc
from rom.addresses import Addresses

# ROM option are a byte long at most, and used for some VARIA patches configuration

class Option(object):
    def __init__(self, addr, mask):
        self.addr = addr
        self.mask = mask

class RomOptions(object):
    def __init__(self, rom, symbols):
        self._rom = rom
        self._options = {}
        self._values = {}
        self._symbols = symbols
        self.addOption("escapeRandoRemoveEnemies", "rando_escape", "opt_remove_enemies")
        self.addOption("backupSaves", "credits_varia", "opt_backup")
        self.addOption("escapeTrigger", "objectives", "escape_option")
        self.addOption("escapeTriggerCrateria", "objectives", "objectives_options_mask", mask=0x1)
        self.addOption("objectivesSFX", "objectives", "objectives_options_mask", mask=0x80)

    def _getAddress(self, namespace, label):
        return snes_to_pc(self._symbols.getAddress(namespace, label))

    def addOption(self, name, namespace, label, mask=0xff):
        opt = Option(self._getAddress(namespace, label), mask)
        self._options[name] = opt
        self._values[opt.addr] = 0

    def read(self, name):
        opt = self._options[name]
        val = self._rom.readByte(opt.addr)
        self._values[opt.addr] = val
        return val & opt.mask

    def write(self, name, value):
        opt = self._options[name]
        val = self._values[opt.addr] | (value & opt.mask)
        self._values[opt.addr] = val
        self._rom.writeByte(val, opt.addr)
