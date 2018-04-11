
# the difficulties for each technics
from smbool import SMBool
from rom import RomPatches

class Pickup:
    def __init__(self, majorsPickup, minorsPickup):
        self.majorsPickup = majorsPickup
        self.minorsPickup = minorsPickup

    def _enoughMinorTable(self, smbm, minorType):
        return smbm.haveItemCount(minorType, int(self.minorsPickup[minorType]))

    def enoughMinors(self, smbm, minorLocations):
        if self.minorsPickup == 'all':
            # need them all
            return len(minorLocations) == 0
        elif self.minorsPickup == 'any':
            return True
        else:
            canEnd = smbm.enoughStuffTourian().bool
            return (canEnd
                    and self._enoughMinorTable(smbm, 'Missile')
                    and self._enoughMinorTable(smbm, 'Super')
                    and self._enoughMinorTable(smbm, 'PowerBomb'))

    def enoughMajors(self, smbm, majorLocations):
        # the end condition
        if self.majorsPickup == 'all':
            return len(majorLocations) == 0
        elif self.majorsPickup == 'any':
            return True
        elif self.majorsPickup == 'minimal':
            canResistRainbow = (smbm.haveItemCount('ETank', 3)
                                and smbm.haveItem('Varia')) \
                               or smbm.haveItemCount('ETank', 6)
            
            return (smbm.haveItem('Morph')
                    # pass bomb block passages
                    and (smbm.haveItem('Bomb')
                         or smbm.haveItem('PowerBomb'))
                    # mother brain rainbow attack
                    and canResistRainbow
                    # lower norfair access
                    and (smbm.haveItem('Varia') or smbm.wnot(RomPatches.has(RomPatches.NoGravityEnvProtection)).bool) # gravity is checked below
                    # speed or ice to access botwoon
                    and (smbm.haveItem('SpeedBooster')
                         or smbm.haveItem('Ice'))
                    # draygon access
                    and smbm.haveItem('Gravity'))
        else:
            return False

class Bosses:
    # bosses helpers to know if they are dead
    areaBosses = {
        'Brinstar': 'Kraid',
        'Norfair': 'Ridley',
        'LowerNorfair': 'Ridley',
        'WreckedShip': 'Phantoon',
        'Maridia': 'Draygon'
    }

    golden4Dead = {
        'Kraid' : False,
        'Phantoon' : False,
        'Draygon' : False,
        'Ridley' : False
    }

    @staticmethod
    def reset():
        for boss in Bosses.golden4Dead:
            Bosses.golden4Dead[boss] = False

    @staticmethod
    def bossDead(boss):
        return SMBool(Bosses.golden4Dead[boss], 0)

    @staticmethod
    def beatBoss(boss):
        Bosses.golden4Dead[boss] = True

    @staticmethod
    def areaBossDead(area):
        if area not in Bosses.areaBosses:
            return True
        return Bosses.golden4Dead[Bosses.areaBosses[area]]

    @staticmethod
    def allBossesDead(smbm):
        return smbm.wand(Bosses.bossDead('Kraid'),
                         Bosses.bossDead('Phantoon'),
                         Bosses.bossDead('Draygon'),
                         Bosses.bossDead('Ridley'))
