import time
import utils.log

class RuntimeLimiter:
    def __init__(self, limit):
        # limit in second, -1 or 0 means no time limit
        self.limit = limit
        self.startTime = time.process_time()
        self.log = utils.log.get('RuntimeLimiter')
        
    def expired(self):
        if self.limit <= 0:
            return False
        if time.process_time() - self.startTime > self.limit:
            self.log.debug("time limit {}s exceeded".format(self.limit))
            return True
        return False
