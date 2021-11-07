from web.backend.utils import transformStats, zipStats
from utils.db import DB

from gluon.http import redirect
from gluon.html import URL

class ProgSpeedStats(object):
    def __init__(self, session, request):
        self.session = session
        self.request = request

        self.vars = self.request.vars

    def run(self):
        self.initProgSpeedStatsSession()

        if self.vars.action == 'Load':
            (ok, msg) = self.validateProgSpeedStatsParams()
            if not ok:
                self.session.flash = msg
                redirect(URL(r=self.request, f='progSpeedStats'))

            self.updateProgSpeedStatsSession()

            skillPreset = "Season_Races"
            randoPreset = "Season_Races"
            majorsSplit = self.vars.majorsSplit

            with DB() as db:
                progSpeedStatsRaw = {}
                progSpeedStats = {}
                progSpeedStats["open14"] = {}
                progSpeedStats["open24"] = {}
                progSpeedStats["open34"] = {}
                progSpeedStats["open44"] = {}
                progSpeeds = ['speedrun', 'slowest', 'slow', 'medium', 'fast', 'fastest', 'basic', 'variable', 'total']
                realProgSpeeds = []
                realProgSpeedsName = []
                for progSpeed in progSpeeds:
                    curRandoPreset = "{}_{}_{}".format(randoPreset, majorsSplit, progSpeed)
                    progSpeedStatsRaw[progSpeed] = db.getProgSpeedStat(skillPreset, curRandoPreset)

                    if len(progSpeedStatsRaw[progSpeed]) != 0:
                        progSpeedStats[progSpeed] = {}
                        progSpeedStats[progSpeed]["avgLocs"] = transformStats(progSpeedStatsRaw[progSpeed]["avgLocs"], 50)
                        open14 = transformStats(progSpeedStatsRaw[progSpeed]["open14"])
                        open24 = transformStats(progSpeedStatsRaw[progSpeed]["open24"])
                        open34 = transformStats(progSpeedStatsRaw[progSpeed]["open34"])
                        open44 = transformStats(progSpeedStatsRaw[progSpeed]["open44"])
                        progSpeedStats[progSpeed]["open"] = zipStats([open14, open24, open34, open44])
                        progSpeedStats[progSpeed]["open"].insert(0, ['Collected items', '1/4 locations available', '2/4 locations available', '3/4 locations available', '4/4 locations available'])

                        progSpeedStats["open14"][progSpeed] = open14
                        progSpeedStats["open24"][progSpeed] = open24
                        progSpeedStats["open34"][progSpeed] = open34
                        progSpeedStats["open44"][progSpeed] = open44

                        realProgSpeeds.append(progSpeed)
                        if progSpeed == 'total':
                            realProgSpeedsName.append('total_rando')
                        else:
                            realProgSpeedsName.append(progSpeed)

            # avg locs
            if len(realProgSpeeds) > 0:
                progSpeedStats['avgLocs'] = zipStats([progSpeedStats[progSpeed]["avgLocs"] for progSpeed in realProgSpeeds])
                progSpeedStats["avgLocs"].insert(0, ['Available locations']+realProgSpeedsName)

            # prog items
            if len(progSpeedStats["open14"]) > 0:
                progSpeedStats["open14"] = zipStats([progSpeedStats["open14"][progSpeed] for progSpeed in realProgSpeeds])
                progSpeedStats["open14"].insert(0, ['Collected items']+realProgSpeedsName)
                progSpeedStats["open24"] = zipStats([progSpeedStats["open24"][progSpeed] for progSpeed in realProgSpeeds])
                progSpeedStats["open24"].insert(0, ['Collected items']+realProgSpeedsName)
                progSpeedStats["open34"] = zipStats([progSpeedStats["open34"][progSpeed] for progSpeed in realProgSpeeds])
                progSpeedStats["open34"].insert(0, ['Collected items']+realProgSpeedsName)
                progSpeedStats["open44"] = zipStats([progSpeedStats["open44"][progSpeed] for progSpeed in realProgSpeeds])
                progSpeedStats["open44"].insert(0, ['Collected items']+realProgSpeedsName)
        else:
            progSpeedStats = None

        majorsSplit = ['Major', 'Full']

        return dict(majorsSplit=majorsSplit, progSpeedStats=progSpeedStats)

    def initProgSpeedStatsSession(self):
        if self.session.progSpeedStats is None:
            self.session.progSpeedStats = {
                'majorsSplit': 'Major'
            }

    def updateProgSpeedStatsSession(self):
        if self.session.progSpeedStats is None:
            self.session.progSpeedStats = {}

        self.session.progSpeedStats['majorsSplit'] = self.vars.majorsSplit

    def validateProgSpeedStatsParams(self):
        if self.vars.majorsSplit not in ['Full', 'Major']:
                return (False, "Wrong value for majorsSplit, authorized values Full/Major")

        return (True, None)
