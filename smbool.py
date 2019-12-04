# super metroid boolean
class SMBool:
    __slots__ = ('bool', 'difficulty', 'knows', 'items')
    def __init__(self, boolean, difficulty=0, knows=[], items=[]):
        self.bool = boolean
        self.difficulty = difficulty
        self.knows = knows
        self.items = items

    def __repr__(self):
        # to display the smbool as a string
        return 'SMBool({}, {}, {}, {})'.format(self.bool, self.difficulty, self.knows, self.items)

    def __getitem__(self, index):
        # to acces the smbool as [0] for the bool and [1] for the difficulty.
        # required when we load a json preset where the smbool is stored as a list,
        # and we add missing smbools to it, so we have a mix of lists and smbools.
        if index == 0:
            return self.bool
        elif index == 1:
            return self.difficulty

    def __bool__(self):
        # when used in boolean expressions (with and/or/not) (python3)
        return self.bool

    def __nonzero__(self):
        # when used in boolean expressions (with and/or/not) (python2)
        return self.bool

    def __eq__(self, other):
        # for ==
        return self.bool == other

    def __ne__(self, other):
        # for !=
        return self.bool != other
