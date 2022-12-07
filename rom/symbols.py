
import re, os, json

from collections import defaultdict
from rom.addressTypes import ValueSingle
from rom.addresses import Addresses
from rom.rom import snes_to_pc

import utils.log

class Symbols(object):
    def __init__(self, patchAccess=None):
        self.log = utils.log.get('Symbols')
        self._patchAccess = patchAccess
        self._symbols = defaultdict(dict)
        self._symbolsAbsolute = {}
        self._reSymbol = re.compile(r"^(?P<bank>[0-9a-fA-F]{2}):(?P<offset>[0-9a-fA-F]{4})\s+(?P<label>[a-zA-Z]\w*)")
        self._reSection = re.compile(r"^\[\w+\]$")

    def loadAllSymbols(self):
        if self._patchAccess is None:
            self.log.debug("No patch access defined, no symbols auto-load")
            return
        for d in self._patchAccess.symbolsDirs:
            try:
                for f in os.listdir(d):
                    fullPath = os.path.join(d, f)
                    if os.path.splitext(f)[1] == ".sym":
                        self.loadWLA(fullPath)
                    elif os.path.splitext(f)[1] == ".json":
                        self.loadJSON(fullPath)
            except FileNotFoundError:
                self.log.debug("Symbols path "+d+" does not exist")
        self.cleanup()

    # removes duplicate "imported" symbols, with prepended namespaces
    # cleans up only absolute symbols
    def cleanup(self):
        dups = self._findDuplicates()
        for addr, syms in dups.items():
            for sym in syms:
                included = [other for other in syms if other in self._symbolsAbsolute and other.endswith("_"+sym)]
                for inc in included:
                    self.log.debug("Deleting absolute symbol "+inc)
                    del self._symbolsAbsolute[inc]

    def _findDuplicates(self):
        return {address:[sym for sym,addr in self._symbolsAbsolute.items() if addr == address] for address in self._symbolsAbsolute.values()}

    def loadWLA(self, wlaPath, namespace=None):
        if namespace is None:
            namespace = os.path.splitext(os.path.basename(wlaPath))[0]
        self.log.debug("* Loading symbols from %s into namespace %s ..." % (wlaPath, namespace))
        with open(wlaPath, "r") as wla:
            labels = False
            while not labels:
                line = wla.readline()
                if line == "":
                    break
                labels = (line.strip() == "[labels]")
            if not labels:
                self.log.warning("No [labels] section found in "+wlaPath)
                return
            while True:
                line = wla.readline()
                if line == "":
                    break
                line = line.strip()
                if self._reSection.match(line) is not None:
                    break
                m = self._reSymbol.match(line)
                if m is not None:
                    addr = int(m.group('bank'), 16) << 16 | int(m.group('offset'), 16)
                    self.addSymbol(namespace, m.group('label'), addr)

    def loadJSON(self, jsonPath, namespace=None):
        if namespace is None:
            namespace = os.path.splitext(os.path.basename(jsonPath))[0]
        self.log.debug("* Loading symbols from %s into namespace %s ..." % (jsonPath, namespace))
        with open(jsonPath, "r") as f:
            syms = json.load(f)
            for sym,addr in syms.items():
                self.addSymbol(namespace, sym, addr)

    def appendToMSL(self, mslPath, symbolsAbsolute=None):
        if symbolsAbsolute is None:
            symbolsAbsolute = self.getAbsoluteSymbols()
        with open(mslPath, "a") as msl:
            for sym in symbolsAbsolute:
                addr = self._symbolsAbsolute[sym]
                msl.write("PRG:%X:%s\n" % (snes_to_pc(addr), sym))

    @staticmethod
    def getAbsoluteSymbolName(namespace, label):
        return "%s_%s" % (namespace, label)

    def writeSymbolsASM(self, asmPath, namespace=None):
        if namespace is None:
            namespace = os.path.splitext(os.path.basename(asmPath))[0]
        with open(asmPath, "w") as asm:
            asm.write("include\n\n")
            for label,addr in self._symbols[namespace].items():
                asm.write("org $%06x\n%s:\n\n" % (addr, Symbols.getAbsoluteSymbolName(namespace, label)))

    def writeSymbolsJSON(self, jsonPath, namespace=None):
        if namespace is None:
            namespace = os.path.splitext(os.path.basename(jsonPath))[0]
        with open(jsonPath, "w") as f:
            json.dump(self._symbols[namespace], f, indent=4)

    def addSymbol(self, namespace, label, addr):
        absSymName = Symbols.getAbsoluteSymbolName(namespace, label)
        self.log.debug("- adding label %s to namespace %s (absolute name: %s) : $%06x" % (label, namespace, absSymName, addr))
        self._symbols[namespace][label] = addr
        self._symbolsAbsolute[absSymName] = addr

    def getAddress(self, namespaceOrAbsoluteSymbol, localSymbol=None):
        if localSymbol is None:
            addr = self._symbolsAbsolute.get(namespaceOrAbsoluteSymbol)
        else:
            addr = self._symbols[namespaceOrAbsoluteSymbol].get(localSymbol)
        return addr

    def getAddresses(self, absoluteSymbolRegexPattern):
        return {sym:self._symbolsAbsolute[sym] for sym in self._symbolsAbsolute if re.match(absoluteSymbolRegexPattern, sym)}

    def getAbsoluteSymbols(self):
        return self._symbolsAbsolute.keys()
