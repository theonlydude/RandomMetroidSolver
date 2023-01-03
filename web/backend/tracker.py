import zlib

from web.backend.utils import raiseHttp, loadPresetsList, transition2isolver, locName4isolver, getAddressesToRead
from web.backend.ws import WS
from graph.graph_utils import vanillaTransitions, vanillaBossesTransitions, vanillaEscapeTransitions, GraphUtils
from graph.vanilla.graph_access import accessPoints
from solver.interactiveSolver import InteractiveSolver
from logic.logic import Logic
from rom.flavor import RomFlavor
from rom.romreader import RomReader

from gluon.html import OPTGROUP

import json

def get_app_files():
    with open('applications/solver/static/client/manifest.json', 'r') as manifest:
        data = json.loads(manifest.read())
    js = [
        "app.js",
        "chunk-vendors.js",
    ]
    css = [
        "app.css",
        "chunk-vendors.css",
    ]
    fa = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.css"
    return '\n'.join([
        *[f'<script src="{data[f]}"></script>' for f in js],
        *[f'<link href="{data[f]}" rel="stylesheet" />' for f in css],
        f'<link href="{fa}" rel="stylesheet" />',
    ])

class Tracker(object):
    def __init__(self, session, request, cache, response):
        self.session = session
        self.request = request
        self.cache = cache
        self.response = response
        # required for GraphUtils access to access points
        # TODO will have to be changed when handling mirror/rotation etc
        flavor = "vanilla"
        Logic.factory(flavor)
        RomFlavor.factory()

    def run(self):
        # init session
        if self.session.tracker is None:
            self.session.tracker = {
                "state": {},
                "preset": "regular",
                "seed": None,
                "startLocation": "Landing Site",
                "logic": "vanilla",
                # set to False in tracker.html
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
        startAPs = GraphUtils.getStartAccessPointNamesCategory()
        startAPs = [OPTGROUP(_label="Standard", *startAPs["regular"]),
                    OPTGROUP(_label="Custom", *startAPs["custom"]),
                    OPTGROUP(_label="Custom (Area rando only)", *startAPs["area"])]

        # get ap -> grapharea for auto tracker
        apsGraphArea = {locName4isolver(ap.Name): ap.GraphArea for ap in accessPoints}

        return dict(stdPresets=stdPresets, tourPresets=tourPresets, comPresets=comPresets,
                    vanillaAPs=vanillaAPs, vanillaBossesAPs=vanillaBossesAPs, escapeAPs=escapeAPs,
                    curSession=self.session.tracker, addresses=addresses, startAPs=startAPs,
                    areaAccessPoints=InteractiveSolver.areaAccessPoints,
                    bossAccessPoints=InteractiveSolver.bossAccessPoints,
                    escapeAccessPoints=InteractiveSolver.escapeAccessPoints,
                    nothingScreens=InteractiveSolver.nothingScreens,
                    doorsScreen=InteractiveSolver.doorsScreen,
                    bossBitMasks=InteractiveSolver.bossBitMasks,
                    apsGraphArea=apsGraphArea, flavorPatches=RomReader.flavorPatches,
                    app_files=get_app_files())

    def trackerWebService(self):
        # unified web service for item/area trackers
        ws = WS.factory(self)
        ws.validate()

        ret = ws.action()
        if ret is None:
            # return something
            raiseHttp(200, "OK", True)
        else:
            if 'deflate' in self.request.env.http_accept_encoding:
                self.response.headers['Content-Encoding'] = 'deflate'
                return zlib.compress(ret.encode())
            else:
                return ret
