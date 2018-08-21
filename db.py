#!/usr/bin/python

# check if a stats db is available
try:
    import mysql.connector
    from db_params import dbParams
    dbAvailable = True
except:
    dbAvailable = False

class DB:
    def __init__(self):
        self.dbAvailable = dbAvailable
        if self.dbAvailable == False:
            return

        try:
            self.conn = mysql.connector.connect(**dbParams)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("DB.__init__::error connect/create cursor: {}".format(e))
            self.dbAvailable = False

    def close(self):
        if self.dbAvailable == False:
            return

        try:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print("DB.close::error: {}".format(e))

    # write data
    def initSolver(self):
        if self.dbAvailable == False:
            return None

        try:
            sql = "insert into solver (action_time) values (now());"
            self.cursor.execute(sql)
            return self.cursor.lastrowid
        except Exception as e:
            print("DB.initSolver::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def addSolverParams(self, id, romFileName, preset, difficultyTarget, pickupStrategy, itemsForbidden):
        if self.dbAvailable == False or id == None:
            return

        try:
            sql = "insert into solver_params values (%d, '%s', '%s', %d, '%s');" % (id, romFileName, preset, difficultyTarget, pickupStrategy)
            self.cursor.execute(sql)

            sql = "insert into solver_items_forbidden values (%d, '%s');"
            for item in itemsForbidden:
                self.cursor.execute(sql % (id, item))
        except Exception as e:
            print("DB.addSolverParams::error execute: {}".format(e))
            self.dbAvailable = False

    def addSolverResult(self, id, returnCode, duration, result):
        if self.dbAvailable == False:
            return

        def lenNone(var):
            if var == None:
                return 0
            else:
                return len(var)

        try:
            if returnCode == 0:
                sql = "insert into solver_collected_items values (%d, '%s', %d);"
                for item, count in result['collectedItems'].iteritems():
                    if count > 0:
                        self.cursor.execute(sql % (id, item, count))

                sql = "insert into solver_result values (%d, %d, %f, %d, %d, %d, %s, %d, %d, %d, %d, %d);" % (id, returnCode, duration, result['difficulty'], result['knowsUsed'][0], result['knowsUsed'][1], result['itemsOk'], lenNone(result['remainTry']), lenNone(result['remainMajors']), lenNone(result['remainMinors']), lenNone(result['skippedMajors']), lenNone(result['unavailMajors']))
            else:
                sql = "insert into solver_result (id, return_code, duration) values (%d, %d, %f);" % (id, returnCode, duration)

            self.cursor.execute(sql)
        except Exception as e:
            print("DB.addSolverResult::error execute \"{}\" error: {}".format(sql, e))
            self.dbAvailable = False

    def initRando(self):
        if self.dbAvailable == False:
            return None

        try:
            sql = "insert into randomizer (action_time) values (now());"
            self.cursor.execute(sql)
            return self.cursor.lastrowid
        except Exception as e:
            print("DB.initRando::error execute: {} error: {}".format(sql, e))
            self.dbAvailable = False

    def addRandoParams(self, id, params):
        if self.dbAvailable == False:
            return None

        # extract the parameters for the database
        dbParams = []
        skipParams = ['output', 'param', 'controls']
        superFuns = []
        i = 2 # skip first parameters (python2 and randomizer.py)
        while i < len(params):
            if params[i][0:len('--')] == '--':
                paramName = params[i][len('--'):]
                if i != len(params) - 1 and params[i+1][0:len('--')] != '--':
                    paramValue = params[i+1]
                    i += 2
                else:
                    paramValue = None
                    i += 1
                if paramName in skipParams:
                    continue
                elif paramName == 'superFun':
                    superFuns.append(paramValue)
                else:
                    dbParams.append((paramName, paramValue))
            elif params[i][0:len('-')] == '-':
                # patch -c, TODO: store them
                i += 2
            else:
                # shouldn't happen
                print("DB.addRandoParams unknown param: {}".format(params[i]))
                i += 1
        if len(superFuns) > 0:
            dbParams.append(('superFun', " ".join(superFuns)))

        try:
            sql = "insert into randomizer_params values (%d, '%s', '%s');"
            for (name, value) in dbParams:
                self.cursor.execute(sql % (id, name, value))
        except Exception as e:
            print("DB.addRandoParams::error execute: {}".format(e))
            self.dbAvailable = False

    def addRandoResult(self, id, returnCode, duration, msg):
        if self.dbAvailable == False:
            return None

        def escapeMsg(msg):
            return msg.replace("'", "''")

        try:
            msg = escapeMsg(msg)
            sql = "insert into randomizer_result (randomizer_id, return_code, duration, error_msg) values (%d, %d, %f, '%s');"
            self.cursor.execute(sql % (id, returnCode, duration, msg))
        except Exception as e:
            print("DB.addRandoResult::error execute \"{}\" error: {}".format(sql, e))
            self.dbAvailable = False

    # read data
    def execSelect(self, sql):
        if self.dbAvailable == False:
            return None

        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            print("DB.execSelect::error execute \"{}\" error: {}".format(sql, e))
            self.dbAvailable = False

    def getUsage(self, table, weeks):
        sql="select date(action_time), count(*) from {} where action_time > DATE_SUB(CURDATE(), INTERVAL {} WEEK) group by date(action_time) order by 1;".format(table, weeks)
        return self.execSelect(sql)

    def getSolverUsage(self, weeks):
        return self.getUsage('solver', weeks)

    def getRandomizerUsage(self, weeks):
        return self.getUsage('randomizer', weeks)

    def getSolverPresets(self, weeks):
        sql="select distinct(sp.preset) from solver s join solver_params sp on s.id = sp.solver_id where s.action_time > DATE_SUB(CURDATE(), INTERVAL {} WEEK);".format(weeks)
        presets = self.execSelect(sql)
        if presets == None:
            return None

        # db returns tuples
        presets = [preset[0] for preset in presets]

        # pivot
        sql="SELECT date(s.action_time)"
        for preset in presets:
            sql += ", SUM(CASE WHEN sp.preset = '{}' THEN 1 ELSE 0 END) AS count_{}".format(preset, preset)
        sql += " FROM solver s join solver_params sp on s.id = sp.solver_id where s.action_time > DATE_SUB(CURDATE(), INTERVAL {} WEEK) GROUP BY date(s.action_time);".format(weeks)

        return (presets, self.execSelect(sql))

    def getSolverResults(self, weeks):
        sql="select date(s.action_time), sr.return_code, count(*) from solver s join solver_result sr on s.id = sr.solver_id where s.action_time > DATE_SUB(CURDATE(), INTERVAL {} WEEK) group by date(s.action_time), sr.return_code order by 1;".format(weeks)
        return self.execSelect(sql)

    def getSolverDurations(self, weeks):
        sql="select s.action_time, sr.duration from solver s join solver_result sr on s.id = sr.solver_id where s.action_time > DATE_SUB(CURDATE(), INTERVAL {} WEEK) order by 1;".format(weeks)
        return self.execSelect(sql)

    def getRandomizerPresets(self, weeks):
        sql="select distinct(value) from randomizer r join randomizer_params rp on r.id = rp.randomizer_id where rp.name = 'preset' and r.action_time > DATE_SUB(CURDATE(), INTERVAL {} WEEK);".format(weeks)
        presets = self.execSelect(sql)
        if presets == None:
            return None

        # db returns tuples
        presets = [preset[0] for preset in presets]

        # pivot
        sql="SELECT date(r.action_time)"
        for preset in presets:
            sql += ", SUM(CASE WHEN rp.value = '{}' THEN 1 ELSE 0 END) AS count_{}".format(preset, preset)
        sql += " FROM randomizer r join randomizer_params rp on r.id = rp.randomizer_id where rp.name = 'preset' and r.action_time > DATE_SUB(CURDATE(), INTERVAL {} WEEK) GROUP BY date(r.action_time);".format(weeks)

        return (presets, self.execSelect(sql))

    def getRandomizerDurations(self, weeks):
        sql="select r.action_time, rr.duration from randomizer r join randomizer_result rr on r.id = rr.randomizer_id where r.action_time > DATE_SUB(CURDATE(), INTERVAL {} WEEK) order by 1;".format(weeks)
        return self.execSelect(sql)

    def getSolverData(self, weeks):
        # return all data csv style
        sql="""select s.id, s.action_time,
sp.romFileName, sp.preset, sp.difficultyTarget, sp.pickupStrategy,
sr.return_code, lpad(round(sr.duration, 2), 5, '0'), sr.difficulty, sr.knows_used, sr.knows_known, sr.items_ok, sr.len_remainTry, sr.len_remainMajors, sr.len_remainMinors, sr.len_skippedMajors, sr.len_unavailMajors,
sci.collected_items,
sif.forbidden_items
from solver s
  left join solver_params sp on s.id = sp.solver_id
  left join solver_result sr on s.id = sr.solver_id
  left join (select solver_id, group_concat(\"(\", item, \", \", count, \")\" order by item) as collected_items from solver_collected_items group by solver_id) sci on s.id = sci.solver_id
  left join (select solver_id, group_concat(item order by item) as forbidden_items from solver_items_forbidden group by solver_id) sif on s.id = sif.solver_id
where s.action_time > DATE_SUB(CURDATE(), INTERVAL {} WEEK)
order by s.id;""".format(weeks)

        header=["id", "actionTime", "romFileName", "preset", "difficultyTarget", "pickupStrategy", "returnCode", "duration", "difficulty", "knowsUsed", "knowsKnown", "itemsOk", "remainTry", "remainMajors", "remainMinors", "skippedMajors", "unavailMajors", "collectedItems", "forbiddenItems"]
        return (header, self.execSelect(sql))

    def getRandomizerData(self, weeks):
        sql="""select r.id, r.action_time,
rr.return_code, lpad(round(rr.duration, 2), 5, '0'), rr.error_msg,
rp.params
from randomizer r
  left join (select randomizer_id, group_concat(\"'\", name, \"': '\", value, \"'\" order by name) as params from randomizer_params group by randomizer_id) rp on r.id = rp.randomizer_id
  left join randomizer_result rr on r.id = rr.randomizer_id
where r.action_time > DATE_SUB(CURDATE(), INTERVAL {} WEEK)
order by r.id;""".format(weeks)

        data = self.execSelect(sql)
        if data == None:
            return None

        outData = []
        paramsSet = set()
        for row in data:
            params = row[5]
            dictParams = eval('{' + params + '}')
            outData.append(row[0:-1] + (dictParams,))
            paramsSet.update(dictParams.keys())

        # custom sort of the params
        paramsHead = []
        for param in ['seed', 'complexity', 'preset', 'area', 'fullRandomization', 'progressionSpeed', 'maxDifficulty', 'morphPlacement', 'spreadItems', 'suitsRestriction', 'energyQty', 'minorQty', 'missileQty', 'superQty', 'powerBombQty', 'progressionDifficulty']:
            if param in paramsSet:
                paramsHead.append(param)
                paramsSet.remove(param)

        header = ["id", "actionTime", "returnCode", "duration", "errorMsg"]
        return (header, outData, paramsHead + sorted(list(paramsSet)))
