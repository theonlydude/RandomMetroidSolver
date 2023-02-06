from logic.logic import Logic
from patches.patchaccess import PatchAccess
from rom.symbols import Symbols
from rom.addresses import Addresses
from utils.doorsmanager import DoorsManager

class RomFlavor(object):
    flavor = None
    symbols = None
    patchAccess = None
    manager = None

    @staticmethod
    def factory():
        RomFlavor.flavor = Logic.implementation
        RomFlavor.patchAccess = PatchAccess()
        RomFlavor.symbols = Symbols(RomFlavor.patchAccess)
        RomFlavor.symbols.loadAllSymbols()
        Addresses.updateFromSymbols(RomFlavor.symbols)
        DoorsManager.setDoorsAddress(RomFlavor.symbols)
        Logic.postSymbolsLoad()
        RomFlavor.patchAccess.postSymbolsLoad()
