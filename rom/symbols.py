
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
        self._reExport = re.compile(r"^export__([A-Za-z0-9_]+)$")

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
        # build reverse dict using defaultdict to read symbols only once
        addrs = defaultdict(list)
        for sym,addr in self._symbolsAbsolute.items():
            addrs[addr].append(sym)
        return addrs

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
                if "freespace_alloc_" in sym:
                    continue
                addr = self._symbolsAbsolute[sym]
                msl.write("PRG:%X:%s\n" % (snes_to_pc(addr), sym))

    @staticmethod
    def getAbsoluteSymbolName(namespace, label):
        return "%s_%s" % (namespace, label)

    def _filterExport(self, namespace):
        return {self._reExport.sub(r"\1", sym):addr for sym,addr in self._symbols[namespace].items() if self._reExport.match(sym)}

    def writeSymbolsASM(self, asmPath, namespace=None, export=False):
        if namespace is None:
            namespace = os.path.splitext(os.path.basename(asmPath))[0]
        syms = self._symbols[namespace] if not export else self._filterExport(namespace)
        with open(asmPath, "w") as asm:
            asm.write("include\n\n")
            for label,addr in syms.items():
                asm.write("org $%06x\n%s:\n\n" % (addr, Symbols.getAbsoluteSymbolName(namespace, label)))

    def writeSymbolsJSON(self, jsonPath, namespace=None, export=True):
        if namespace is None:
            namespace = os.path.splitext(os.path.basename(jsonPath))[0]
        syms = self._symbols[namespace] if not export else self._filterExport(namespace)
        if not syms:
            return False
        with open(jsonPath, "w") as f:
            json.dump(syms, f, indent=4)
        return True

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

    def getAddresses(self, namespace, localSymbolRegexPattern):
        return {sym:self._symbols[namespace][sym] for sym in self._symbols[namespace] if re.match(localSymbolRegexPattern, sym)}

    def getAbsoluteSymbols(self):
        return self._symbolsAbsolute.keys()

    def getNamespaces(self):
        return self._symbols.keys()

    def getLabels(self, namespace):
        return self._symbols[namespace].keys() if namespace in self._symbols else None


class Freespace(object):
    def __init__(self, symbols, base=["vanilla_freespace"]):
        self.log = symbols.log
        self._symbols = symbols
        self.freespace = self._loadFreespace(base)
        self.allocs = self._loadAllocs(base)
        self.bankLayouts = self._buildBankLayouts()

    def _getRanges(self, ret, namespace):
        labels = self._symbols.getLabels(namespace)
        if labels is None:
            return ret
        allocStarts = [label for label in labels if label.startswith("freespace_alloc_start_")]
        allocEnds = [label for label in labels if label.startswith("freespace_alloc_end_")]
        assert len(allocStarts) >= len(allocEnds)
        allocIdx = lambda label: int(label.split('_')[-1])
        getBank = lambda addr: addr >> 16
        for start in allocStarts:
            i = allocIdx(start)
            startAddr = self._symbols.getAddress(namespace, start)
            startBank = getBank(startAddr)
            endLabel = "freespace_alloc_end_" + str(i)
            endAddr = self._symbols.getAddress(namespace, endLabel) if endLabel in allocEnds else None
            if endAddr is None:
                self.log.warning("No end for freespace alloc %d in namespace %s (addr: $%06x)" % (i, namespace, startAddr))
                # try to find the next closest freespace in the same bank
                endAddr = startAddr | 0xffff # end bank if not found
                for possibleEnd in allocStarts:
                    if possibleEnd == start:
                        continue
                    addr = self._symbols.getAddress(namespace, possibleEnd)
                    if getBank(addr) != startBank:
                        continue
                    if addr >= startAddr and addr < endAddr:
                        self.log.debug("Selected %s for alloc %d end in namespace %s (addr: $%06x)" % (possibleEnd, i, namespace, addr))
                        endAddr = addr
                self.log.info("Selected $%06x as end" % endAddr)
            assert startBank == getBank(endAddr)
            self.log.debug("Freespace alloc %d in namespace %s : ($%06x, $%06x)" % (i, namespace, startAddr, endAddr))
            ret[startBank].append((startAddr, endAddr))

    def _loadFreespace(self, freespaceDefs):
        ranges = defaultdict(list)
        for namespace in freespaceDefs:
            self._getRanges(ranges, namespace)
        return ranges

    def _findContainingFreespace(self, start, end):
        for rstart, rend in self.freespace[start >> 16]:
            if rstart <= start and rend >= end:
                return (rstart, rend)
        return None

    def _loadAllocs(self, base):
        ret = {}
        for namespace in self._symbols.getNamespaces():
            if namespace in base:
                continue
            rangesByBank = defaultdict(list)
            self._getRanges(rangesByBank, namespace)
            # find a containing freespace range
            for bank, ranges in rangesByBank.items():
                assert bank in self.freespace, "No freespace defined in bank %02x" % bank
                for start, end in ranges:
                    assert self._findContainingFreespace(start, end) is not None, "No suitable freespace range found in bank %02x for range ($%06x, $%06x)" % (bank, start, end)
            ret[namespace] = rangesByBank
        return ret

    def _buildBankLayouts(self):
        ret = defaultdict(dict)
        for bank in sorted(self.freespace.keys()):
            for start, end in sorted(self.freespace[bank]):
                patches = []
                for namespace, rangesByBank in self.allocs.items():
                    if bank in rangesByBank:
                        patches.append({"patch": namespace, "ranges": [(rs, re) for rs, re in sorted(rangesByBank[bank]) if rs >= start and re <= end]})
                ret[bank][(start, end)] = sorted(patches, key=lambda p: p["ranges"][0])
        return ret

    @property
    def banks(self):
        return list(self.bankLayouts.keys())

    def getSpan(self, bank):
        start, end = bank << 16 | 0xffff, bank << 16 | 0x8000
        for rs, re in self.bankLayouts[bank]:
            if rs < start:
                start = rs
            if re > end:
                end = re
        return (start, end)
