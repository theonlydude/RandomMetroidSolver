# super metroid boolean
class SMBool:
    def __init__(self, bool, difficulty=0, knows=[], items=[]):
        self.bool = bool
        self.difficulty = difficulty
        self.knows = knows
        self.items = items

    def __repr__(self):
        # to display the smbool as a string
        return '({}, {})'.format(self.bool, self.difficulty)

    def __getitem__(self, index):
        # to acces the smbool as [0] for the bool and [1] for the difficulty
        if index == 0:
            return self.bool
        elif index == 1:
            return self.difficulty
