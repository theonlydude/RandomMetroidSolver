

class Restrictions(object):
    def __init__(self, settings):
        self.settings = settings
        self.checkers = self.getCheckers()
        self.split = settings.restrictions['MajorMinor']

    def isEarlyMorph(self):
        return self.settings.restrictions['Morph'] == 'early'

    def isLateMorph(self):
        return self.settings.restrictions['Morph'] == 'late'

    def isLocMajor(self, loc):
        return 'Boss' not in loc['Class'] and (self.split == "Full" or self.split in loc['Class'])

    def isLocMinor(self, loc):
        return 'Boss' not in loc['Class'] and (self.split == "Full" or self.split not in loc['Class'])

    def isItemMajor(self, item):
        if self.split == "Full":
            return True
        else:
            return item['Class'] == self.split

    def isItemMinor(self, item):
        if self.split == "Full":
            return True
        else:
            return item['Class'] == "Minor"

    def isItemLocMatching(item, loc):
        if self.split == "Full":
            return True
        if self.split in loc['Class']:
            return item['Class'] == self.split
        else:
            return item['Class'] == "Minor"

    def lateMorphCheck(self):
        # TODO
        pass

    # TODO add early morph hooks
    
    def getCheckers(self):
        checkers = []
        checkers.append(lambda item, loc: not 'Boss' in loc['Class'] or item['Name'] == loc['Name'])
        if restrictions['MajorMinor'] != 'Full':
            checkers.append(self.isItemLocMatching)
        if restrictions['Suits']:
            checkers.append(lambda item, loc: not isSuit(item) or loc['GraphArea'] != 'Crateroa')
        if self.isLateMorph():
            checkers.append(lambda item, loc: not isMorph(item) or self.lateMorphCheck(location))
        # TODO add checker for random fill is random fill in settings
        return checkers        

    def canPlaceAtLocation(self, item, location):
        ret = True
        for chk in self.checkers:
            ret = ret and chk(item, location)
            if not ret:
                break
        return ret

        # # plando locs are not available
        # if 'itemName' in location:
        #     return False
