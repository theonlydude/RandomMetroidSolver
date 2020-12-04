from utils.parameters import infinity
import copy

class Location:
    graph_slots = (
        'distance', 'accessPoint', 'difficulty', 'path',
        'pathDifficulty', 'locDifficulty' )
    
    rando_slots = (
        'restricted', )

    solver_slots = (
        'itemName', 'comeBack', 'areaWeight' )

    __slots__ = graph_slots + rando_slots + solver_slots

    def __init__(
            self, distance=None, accessPoint=None,
            difficulty=None, path=None, pathDifficulty=None,
            locDifficulty=None, restricted=None, itemName=None,
            itemType=None, comeBack=None, areaWeight=None):
        self.distance = distance
        self.accessPoint = accessPoint
        self.difficulty = difficulty
        self.path = path
        self.pathDifficulty = pathDifficulty
        self.locDifficulty = locDifficulty
        self.restricted = restricted
        self.itemName = itemName
        self.itemType = itemType
        self.comeBack = comeBack
        self.areaWeight = areaWeight

    def isMajor(self):
        return self._isMajor

    def isChozo(self):
        return self._isChozo

    def isMinor(self):
        return self._isMinor

    def isBoss(self):
        return self._isBoss

    def isClass(self, _class):
        return _class in self.Class

    def evalPostAvailable(self, smbm):
        if self.difficulty.bool == True and self.PostAvailable is not None:
            smbm.addItem(self.itemName)
            postAvailable = self.PostAvailable(smbm)
            smbm.removeItem(self.itemName)

            self.difficulty = self.difficulty & postAvailable

    def evalComeBack(self, smbm, areaGraph, ap):
        if self.difficulty.bool == True:
            # check if we can come back to given ap from the location
            self.comeBack = areaGraph.canAccess(smbm, self.accessPoint, ap, infinity, self.itemName)

    def json(self):
        # to return after plando rando
        ret = {'Name': self.Name, 'accessPoint': self.accessPoint}
        if self.difficulty is not None:
            ret['difficulty'] = self.difficulty.json()
        return ret

    def __repr__(self):
        return "Location({}: {})".format(self.Name,
            '. '.join(
                (repr(getattr(self, slot)) for slot in Location.__slots__)))

    def __copy__(self):
        d = self.difficulty
        difficulty = copy.copy(d) if d is not None else None
        ret = type(self)(
            self.distance, self.accessPoint, difficulty, self.path,
            self.pathDifficulty, self.locDifficulty, self.restricted,
            self.itemName, self.itemType, self.comeBack,
            self.areaWeight)

        return ret

def define_location(
        Area, GraphArea, SolveArea, Name, Class, CanHidden, Address, Id,
        Visibility, Room, AccessFrom, Available, PostAvailable=None):
    name = Name.replace(' ', '').replace(',', '') + 'Location'
    subclass = type(name, (Location,), {
        'Area': Area,
        'GraphArea': GraphArea,
        'SolveArea': SolveArea,
        'Name': Name,
        'Class': Class,
        'CanHidden': CanHidden,
        'Address': Address,
        'Id': Id,
        'Visibility': Visibility,
        'Room': Room,
        'AccessFrom': AccessFrom,
        'Available': Available,
        'PostAvailable': PostAvailable,
        '_isMajor': 'Major' in Class,
        '_isChozo': 'Chozo' in Class,
        '_isMinor': 'Minor' in Class,
        '_isBoss': 'Boss' in Class
    })
    return subclass()
