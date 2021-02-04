import sys

# simple heuristic to detect infinite rollbacks and abort randomization sooner.
# the goal is to reduce the duration of the large jm.
class InfiniteRollback(object):
    def __init__(self, startAP, restrictions):
        self.rollbackCount = 0
        self.steps = ""
        # the repeating patterns to check
        self.primes = [1, 2, 3]
        # wait until detectThreshold rollbacks happened before detecting infinite rollbacks
        self.detectThreshold = self.primes[-1]*2+1
        # also wait for a minimum number of steps to avoid false positives with startup rollbacks.
        stepByAp = {
            "Mama Turtle": 2048,
            "Green Brinstar Elevator": 1536,
            "Aqueduct": 512
        }
        self.minimumSteps =  stepByAp[startAP] if startAP in stepByAp else 256
        if restrictions.isChozo():
            # set quite high because chozo can do a lot of rollbacks at startup.
            self.minimumSteps = 2048
        if restrictions.isLateMorph():
            # most infinite rollback are caused by late morph, so putting a high value here
            # prevents false positive, but also reduce the interest of this heuristic and
            # the time that can be gained during jm...
            self.minimumSteps = 2048
        self.rollbackIndexes = []
        # when we suspect an infinite rollback validate it with confirmationThreshold rollbacks
        self.suspicion = False
        self.confirmationCount = 0
        self.confirmationThreshold = 10

    def addStep(self, step):
        self.steps += step

    def addRollback(self, rollback):
        # return True if an infinite rollback is detected
        self.rollbackIndexes.append(len(self.steps))
        self.steps += rollback
        self.rollbackCount += 1

        if self.rollbackCount < self.detectThreshold or len(self.steps) < self.minimumSteps:
            return False

        # check for repeating patterns
        found = False
        for prime in self.primes:
            pattern = self.steps[self.rollbackIndexes[-prime-1]:self.rollbackIndexes[-1]]
            doublePattern = self.steps[self.rollbackIndexes[-prime*2-1]:self.rollbackIndexes[-1]]
            if doublePattern == pattern * 2:
                found = True
                break

        if found:
            if self.suspicion == True:
                self.confirmationCount += 1
                if self.confirmationCount >= self.confirmationThreshold:
                    # write it in the log
                    sys.stdout.write('i')
                    sys.stdout.flush()
                    return True
            else:
                self.suspicion = True
        elif self.suspicion == True:
            self.suspicion = False
            self.confirmationCount = 0

        return False
