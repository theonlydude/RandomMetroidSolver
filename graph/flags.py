from enum import IntFlag, auto

class BossAccessPointFlags(IntFlag):
    G4 = auto()
    MiniBoss = auto()
    Inside = auto()
    Backdoor = auto()
    Split = auto() # this is not a transition flag, but rather a randomization mode
