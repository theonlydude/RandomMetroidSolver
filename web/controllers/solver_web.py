# -*- coding: utf-8 -*-
import sys, os.path

for base in ['~/RandomMetroidSolver', '~/web2py']:
    path = os.path.expanduser(base)
    if path not in sys.path:
        sys.path.append(path)

# put an expiration date to the default cookie to have it kept between browser restart
response.cookies['session_id_solver']['expires'] = 31 * 24 * 3600
response.title = 'Super Metroid VARIA Randomizer, Solver and Trackers'

def home():
    session.forget(response)
    return dict()

def solver():
    from web.backend.solver import Solver
    return Solver(session, request, cache).run()

def infos():
    session.forget(response)
    return dict()


def randomizer():
    from web.backend.randomizer import Randomizer
    return Randomizer(session, request, response, cache).run()

def randomizerWebService():
    session.forget(response)
    # set header to authorize cross domain AJAX
    response.headers['Access-Control-Allow-Origin'] = '*'
    from web.backend.randomizer import Randomizer
    return Randomizer(session, request, response, cache).webService()

def presetWebService():
    session.forget(response)
    from web.backend.randomizer import Randomizer
    return Randomizer(session, request, response, cache).presetWebService()

def sessionWebService():
    from web.backend.randomizer import Randomizer
    return Randomizer(session, request, response, cache).sessionWebService()

def randoPresetWebService():
    from web.backend.randomizer import Randomizer
    return Randomizer(session, request, response, cache).randoPresetWebService()

def randoParamsWebService():
    session.forget(response)
    from web.backend.randomizer import Randomizer
    return Randomizer(session, request, response, cache).randoParamsWebService()


def presets():
    from web.backend.presets import Presets
    return Presets(session, request, cache).run()

def skillPresetActionWebService():
    from web.backend.presets import Presets
    return Presets(session, request, cache).skillPresetActionWebService()

def skillPresetListWebService():
    session.forget(response)
    from web.backend.presets import Presets
    return Presets(session, request, cache).skillPresetListWebService()


def tracker():
    from web.backend.tracker import Tracker
    return Tracker(session, request, cache, response).run()

def plando():
    from web.backend.plando import Plando
    return Plando(session, request, cache).run()

def trackerWebService():
    from web.backend.tracker import Tracker
    return Tracker(session, request, cache, response).trackerWebService()


def customizer():
    from web.backend.customizer import Customizer
    return Customizer(session, request, cache).run()

def customWebService():
    from web.backend.customizer import Customizer
    return Customizer(session, request, cache).customWebService()

def getSpcFile():
    session.forget(response)
    from web.backend.customizer import Customizer
    return Customizer(session, request, cache).getSpcFile()


def stats():
    session.forget(response)
    from web.backend.stats import Stats
    return Stats().run()

def extStats():
    from web.backend.extStats import ExtStats
    return ExtStats(session, request, cache).run()

def progSpeedStats():
    from web.backend.progSpeedStats import ProgSpeedStats
    return ProgSpeedStats(session, request).run()


def plandorepo():
    session.forget(response)
    from web.backend.plandorepo import PlandoRepo
    return PlandoRepo(request).run()

def plandoRateWebService():
    session.forget(response)
    from web.backend.plandorepo import PlandoRepo
    return PlandoRepo(request).plandoRateWebService()

def downloadPlandoWebService():
    session.forget(response)
    from web.backend.plandorepo import PlandoRepo
    return PlandoRepo(request).downloadPlandoWebService()

def uploadPlandoWebService():
    session.forget(response)
    from web.backend.plandorepo import PlandoRepo
    return PlandoRepo(request).uploadPlandoWebService()

def deletePlandoWebService():
    session.forget(response)
    from web.backend.plandorepo import PlandoRepo
    return PlandoRepo(request).deletePlandoWebService()

def updatePlandoWebService():
    session.forget(response)
    from web.backend.plandorepo import PlandoRepo
    return PlandoRepo(request).updatePlandoWebService()


def _redirect():
    redirect(URL(request.env.path_info, r=request, scheme=True, host="randommetroidsolver.pythonanywhere.com"))
