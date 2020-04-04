from smbool import SMBool

# layout patches added by randomizers
class RomPatches:
    #### Patches definitions

    ### Layout
    # blue door to access the room with etank+missile
    BlueBrinstarBlueDoor      = 10
    # missile in the first room is a major item and accessible and ceiling is a minor
    BlueBrinstarMissile       = 11
    # shot block instead of bomb blocks for spazer access
    SpazerShotBlock           = 20
    # climb back up red tower from bottom no matter what
    RedTowerLeftPassage       = 21
    # exit red tower top to crateria
    RedTowerBlueDoors         = 22
    # shot block in crumble blocks at early supers
    EarlySupersShotBlock      = 23
    # brinstar reserve area door blue
    BrinReserveBlueDoors      = 24
    # red tower top PB door to hellway
    HellwayBlueDoor           = 25
    # etecoon supers blue door
    EtecoonSupersBlueDoor     = 26
    # shot block to exit hi jump area
    HiJumpShotBlock           = 30
    # access main upper norfair without anything
    CathedralEntranceWallJump = 31
    # graph blue doors
    HiJumpAreaBlueDoor        = 32
    SpeedAreaBlueDoors        = 33
    # moat bottom block
    MoatShotBlock             = 41
    #graph
    SpongeBathBlueDoor        = 42
    # maridia
    MaridiaTubeOpened         = 51
    MamaTurtleBlueDoor        = 52,
    ## Area rando patches
    # remove crumble block for reverse lower norfair door access
    SingleChamberNoCrumble    = 101
    # remove green gates for reverse maridia access
    AreaRandoGatesBase        = 102
    # remove crab green gate in maridia and blue gate in green brinstar
    AreaRandoGatesOther       = 103
    # disable Green Hill Yellow, Noob Bridge Green, Coude Yellow, and Kronic Boost yellow doors
    AreaRandoBlueDoors        = 104
    # crateria key hunter yellow, green pirates shaft red
    AreaRandoMoreBlueDoors    = 105

    ### Other
    # Gravity no longer protects from environmental damage (heat, spikes...)
    NoGravityEnvProtection  = 1000
    # Wrecked Ship etank accessible when Phantoo is alive
    WsEtankPhantoonAlive    = 1001
    # Lower Norfair chozo (vanilla access to GT/Screw Area) : disable space jump check
    LNChozoSJCheckDisabled  = 1002
    # Progressive suits patch, mutually exclusive with NoGravityEnvProtection
    ProgressiveSuits        = 1003
    # Nerfed charge beam available from the start
    NerfedCharge            = 1004

    #### Patch sets
    # total randomizer
    TotalBase = [ BlueBrinstarBlueDoor, RedTowerBlueDoors, NoGravityEnvProtection ]
    # tournament and full
    TotalLayout = [ MoatShotBlock, EarlySupersShotBlock,
                    SpazerShotBlock, RedTowerLeftPassage,
                    HiJumpShotBlock, CathedralEntranceWallJump ]

    Total = TotalBase + TotalLayout

    # casual
    TotalCasual = [ BlueBrinstarMissile ] + Total

    # area rando patch set
    AreaSet = [ SingleChamberNoCrumble, AreaRandoGatesBase, AreaRandoGatesOther, AreaRandoBlueDoors, AreaRandoMoreBlueDoors ]

    # VARIA specific patch set
    VariaTweaks = [ WsEtankPhantoonAlive, LNChozoSJCheckDisabled ]

    # dessyreqt randomizer
    Dessy = []

    ### Active patches
    ActivePatches = []

    @staticmethod
    def has(patch):
        return SMBool(patch in RomPatches.ActivePatches)

    @staticmethod
    def setDefaultPatches(startAP):
        # called by the isolver in seedless mode.
        # activate only layout patch (the most common one), red tower blue doors and the startAP's patches.
        from graph_access import GraphUtils
        RomPatches.ActivePatches = [RomPatches.RedTowerBlueDoors] + RomPatches.TotalLayout + GraphUtils.getGraphPatches(startAP)
