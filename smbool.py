# super metroid boolean
class SMBool:
    def __init__(self, bool, difficulty=0, knows=[], items=[]):
        # to avoid storing an SMBool as the bool attribute of the SMBool
        if bool == True:
            self.bool = True
        else:
            self.bool = False
        self.difficulty = difficulty
        self.knows = knows
        self.items = items

    def __repr__(self):
        # to display the smbool as a string
        return 'SMBool({}, {})'.format(self.bool, self.difficulty)

    def __getitem__(self, index):
        # to acces the smbool as [0] for the bool and [1] for the difficulty
        if index == 0:
            return self.bool
        elif index == 1:
            return self.difficulty

    def __bool__(self):
        # when used in boolean expressions (with and/or/not) (python3)
        return self.bool

    def __nonzero__(self):
        # when used in boolean expressions (with and/or/not) (python2)
        return self.bool == True

    def __eq__(self, other):
        # for ==
        return self.bool == other

    def __ne__(self, other):
        # for !=
        return self.bool != other
