from logic.logic import Logic
from patches.patchaccess import PatchAccess
from rom.symbols import Symbols
from rom.addresses import Addresses
from utils.doorsmanager import DoorsManager
from multiprocessing.managers import BaseManager

class SymbolsManager(BaseManager):
    pass

class RomFlavor(object):
    flavor = None
    symbols = None
    patchAccess = None
    manager = None

    ports = {
        "vanilla": 25001,
        "mirror": 25002
    }

    @staticmethod
    def factory(remote=False):
        RomFlavor.flavor = Logic.implementation
        RomFlavor.patchAccess = PatchAccess()
        if not remote:
            RomFlavor.symbols = Symbols(RomFlavor.patchAccess)
            RomFlavor.symbols.loadAllSymbols()
        else:
            RomFlavor.manager = SymbolsManager(address=("localhost", RomFlavor.ports[RomFlavor.flavor]), authkey=b'password')
            RomFlavor.manager.register("Symbols")
            RomFlavor.manager.connect()
            RomFlavor.symbols = RomFlavor.manager.Symbols()
        Addresses.updateFromSymbols(RomFlavor.symbols)
        DoorsManager.setDoorsAddress(RomFlavor.symbols)
