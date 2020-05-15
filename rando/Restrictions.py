

class Restrictions(object):
    def __init__(self, settings, services):
        self.settings = settings
        self.services = services
        self.checkers = self.getCheckers()

    def isItemLocMatching(item, loc):
        if self.restrictions['MajorMinor'] in loc['Class']:
            return item['Class'] == self.restrictions['MajorMinor']
        else:
            return item['Class'] == "Minor"

    def lateMorphCheck(self):
        # TODO
        pass

    # TODO add early morph hooks
    
    def getCheckers(self):
        checkers = []
        checkers.append(lambda item, loc: not (item['Type'] == 'Boss' and not 'Boss' in location['Class']))
        checkers.append(lambda item, loc: not ('Boss' in location['Class'] and not item['Type'] == 'Boss'))
        if restrictions['MajorMinor'] != 'Full':
            checkers.append(self.isItemLocMatching)
        if restrictions['Suits']:
            checkers.append(lambda item, loc: not isSuit(item) or loc['GraphArea'] != 'Crateroa')
        if self.restrictions['Morph'] == 'late':
            checkers.append(lambda item, loc: not isMorph(item) or self.lateMorphCheck(location))
        # TODO add checker for random fill is random fill in settings
        return checkers        

    def canPlaceAtLocation(self, item, location, checkSoftlock=False):
        ret = True
        for chk in self.checkers:
            ret = ret and chk(item, location)
            if not ret:
                break
        if ret and checkSoftlock == True:
            ret = self.services.isSoftlockPossible(item, location)
        return ret

        # # plando locs are not available
        # if 'itemName' in location:
        #     return False
