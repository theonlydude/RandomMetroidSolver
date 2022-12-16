#!/usr/bin/python3

import sys

from logic.logic import Logic
from rom.flavor import RomFlavor, SymbolsManager
from rom.symbols import Symbols
from patches.patchaccess import PatchAccess
from multiprocessing import Process
from multiprocessing.managers import BaseManager

if len(sys.argv) < 2:
    print("args: logic")
    sys.exit(1)

Logic.factory(sys.argv[1])

symbols = Symbols(PatchAccess())
symbols.loadAllSymbols()
SymbolsManager.register("Symbols", lambda: symbols)

port = RomFlavor.ports[Logic.implementation]
manager = SymbolsManager(address=("localhost", port), authkey=b'password')
server = manager.get_server()
server.serve_forever()
