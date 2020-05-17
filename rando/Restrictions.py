

class Restrictions(object):
    def __init__(self, settings):
        self.settings = settings
        self.checkers = self.getCheckers()

    def isLocMajor(self, loc):
        return 'Boss' not in loc['Class'] and (self.settings.restrictions['MajorMinor'] == "Full" or self.settings.restrictions['MajorMinor'] in loc['Class'])

    def isLocMinor(self, loc):
        return 'Boss' not in loc['Class'] and (self.settings.restrictions['MajorMinor'] == "Full" or self.settings.restrictions['MajorMinor'] not in loc['Class'])

    def isItemMajor(self, item):
        if self.settings.restrictions['MajorMinor'] == "Full":
            return True
        else:
            return item['Class'] == self.settings.restrictions['MajorMinor']

    def isItemMinor(self, item):
        if self.settings.restrictions['MajorMinor'] == "Full":
            return True
        else:
            return item['Class'] == "Minor"

    def isItemLocMatching(item, loc):
        if self.settings.restrictions['MajorMinor'] in loc['Class']:
            return item['Class'] == self.settings.restrictions['MajorMinor']
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
        if self.settings.restrictions['Morph'] == 'late':
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
