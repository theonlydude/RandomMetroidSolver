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

                sql = "insert into solver_result values (%d, %d, %f, %d, %d, %d, '%s', %d, %d, %d, %d, %d);" % (id, returnCode, duration, result['difficulty'], result['knowsUsed'][0], result['knowsUsed'][1], result['itemsOk'], lenNone(result['remainTry']), lenNone(result['remainMajors']), lenNone(result['remainMinors']), lenNone(result['skippedMajors']), lenNone(result['unavailMajors']))
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
        skipParams = ['seed', 'output', 'param', 'controls']
        superFuns = []
        i = 2 # skip first parameters
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
                i += 1
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

        try:
            sql = "insert into randomizer_result (randomizer_id, return_code, duration, error_msg) values (%d, %d, %f, '%s');"
            self.cursor.execute(sql % (id, returnCode, duration, msg))
        except Exception as e:
            print("DB.addRandoResult::error execute \"{}\" error: {}".format(sql, e))
            self.dbAvailable = False
