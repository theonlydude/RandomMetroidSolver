from web.backend.utils import loadPresetsList, transition2isolver, getAddressesToRead, get_client_files
from graph.graph_utils import vanillaTransitions, vanillaBossesTransitions, vanillaEscapeTransitions, GraphUtils
from rom.romreader import RomReader
from utils.version import displayedVersion

from gluon.html import OPTGROUP

class Plando(object):
    def __init__(self, session, request, cache):
        self.session = session
        self.request = request
        self.cache = cache

    def run(self):
        # init session
        if self.session.plando is None:
            self.session.plando = {
                "state": {},
                "preset": "regular",
                "seed": None,
                "startLocation": "Landing Site",
                "logic": "vanilla",

                # rando params
                "rando": {},

                # set to False in plando.html
                "firstTime": True
            }

        # load presets list
        (stdPresets, tourPresets, comPresets) = loadPresetsList(self.cache)

        # access points
        vanillaAPs = []
        for (src, dest) in vanillaTransitions:
            vanillaAPs += [transition2isolver(src), transition2isolver(dest)]

        vanillaBossesAPs = []
        for (src, dest) in vanillaBossesTransitions:
            vanillaBossesAPs += [transition2isolver(src), transition2isolver(dest)]

        escapeAPs = []
        for (src, dest) in vanillaEscapeTransitions:
            escapeAPs += [transition2isolver(src), transition2isolver(dest)]

        # generate list of addresses to read in the ROM
        addresses = getAddressesToRead(self.cache)

        startAPs = GraphUtils.getStartAccessPointNamesCategory('vanilla')
        startAPs = [OPTGROUP(_label="Standard", *startAPs["regular"]),
                    OPTGROUP(_label="Custom", *startAPs["custom"]),
                    OPTGROUP(_label="Custom (Area rando only)", *startAPs["area"])]

        return dict(stdPresets=stdPresets, tourPresets=tourPresets, comPresets=comPresets,
                    vanillaAPs=vanillaAPs, vanillaBossesAPs=vanillaBossesAPs, escapeAPs=escapeAPs,
                    curSession=self.session.plando, addresses=addresses, startAPs=startAPs,
                    version=displayedVersion, flavorPatches=RomReader.flavorPatches,
                    client_files=get_client_files())
