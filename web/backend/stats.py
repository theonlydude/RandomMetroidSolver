import os, glob

from utils.db import DB

class Stats(object):
    def run(self):
        weeks = 1

        with DB() as db:
            solverPresets = db.getSolverPresets(weeks)
            randomizerPresets = db.getRandomizerPresets(weeks)

            solverDurations = db.getSolverDurations(weeks)
            randomizerDurations = db.getRandomizerDurations(weeks)

            solverData = db.getSolverData(weeks)
            randomizerData = db.getRandomizerData(weeks)

            isolver = db.getISolver(weeks)
            isolverData = db.getISolverData(weeks)

            spritesData = db.getSpritesData(weeks)
            shipsData = db.getShipsData(weeks)
            plandoRandoData = db.getPlandoRandoData(weeks)

            randomizerParamsStats = db.getRandomizerParamsStats(weeks)

        errors = self.getErrors()

        (fsStatus, fsPercent) = self.getFsUsage()

        return dict(solverPresets=solverPresets, randomizerPresets=randomizerPresets,
                    solverDurations=solverDurations, randomizerDurations=randomizerDurations,
                    solverData=solverData, randomizerData=randomizerData,
                    randomizerParamsStats=randomizerParamsStats,
                    isolver=isolver, isolverData=isolverData, spritesData=spritesData,
                    shipsData=shipsData, errors=errors,
                    fsStatus=fsStatus, fsPercent=fsPercent, plandoRandoData=plandoRandoData)

    def getErrors(self):
        # check dir exists
        errDir = os.path.expanduser("~/web2py/applications/solver/errors")
        if os.path.isdir(errDir):
            # list error files
            errFiles = glob.glob(os.path.join(errDir, "*"))

            # sort by date
            errFiles.sort(key=os.path.getmtime)
            errFiles = [os.path.basename(f) for f in errFiles]
            return errFiles
        else:
            return []

    def getFsUsage(self):
        fsData = os.statvfs('/home')
        percent = round(100 - (100.0 * fsData.f_bavail / fsData.f_blocks), 2)
        if percent < 80:
            return ('OK', percent)
        elif percent < 95:
            return ('WARNING', percent)
        else:
            return ('CRITICAL', percent)


