# https://github.com/tewtal/itemrandomizerweb/blob/master/ItemRandomizer/TournamentLocations.fs

# Functions to check if we have a specific item
def haveItem(items, itemType):
    return List.exists(lambda item: item["Type"] == itemType, items)

def itemCount(items, itemType):
    return List.length(List.filter(lambda item: item["Type"] == itemType, items))

def energyReserveCount(items):
    return itemCount(items, "ETank") + itemCount(items, "Reserve")

def heatProof(items):
    return haveItem(items, "Varia")

# Combined checks to see if we can perform an action needed to access locations
def canHellRun(items):
    return (energyReserveCount(items) >= 3 or
            heatProof(items))

def canFly(items):
    return (haveItem(items, "Morph") and haveItem(items, "Bomb")) or haveItem(items, "SpaceJump")
def canUseBombs(items):
    return haveItem(items, "Morph") and haveItem(items, "Bomb")

def canOpenRedDoors(items):
    return haveItem(items, "Missile") or haveItem(items, "Super")
def canOpenGreenDoors(items):
    return haveItem(items, "Super")
def canOpenYellowDoors(items):
    return haveItem(items, "Morph") and haveItem(items, "PowerBomb")
def canUsePowerBombs():
    return canOpenYellowDoors()

let canDestroyBombWalls items =
    (haveItem items Morph &&
        (haveItem items Bomb ||
         haveItem items PowerBomb)) ||
    haveItem items ScrewAttack

let canCrystalFlash items = 
    itemCount items Missile >= 2 &&
    itemCount items Super >= 2 &&
    itemCount items PowerBomb >= 3

let canEnterAndLeaveGauntlet items =
    (canFly items || haveItem items HiJump || haveItem items SpeedBooster) &&
    (canUseBombs items || 
     (canUsePowerBombs items && itemCount items PowerBomb >= 2) || 
     haveItem items ScrewAttack ||
     (haveItem items SpeedBooster && canUsePowerBombs items && (energyReserveCount items >= 2)))

let canPassBombPassages items =
    canUseBombs items || 
    canUsePowerBombs items

let canAccessRedBrinstar items =
    haveItem items Super && 
        ((canDestroyBombWalls items && haveItem items Morph) || 
         canUsePowerBombs items)

let canAccessKraid items = 
    canAccessRedBrinstar items &&
    canPassBombPassages items

let canAccessWs items = 
    canUsePowerBombs items && 
    haveItem items Super

let canAccessHeatedNorfair items =
    canAccessRedBrinstar items &&
         (canHellRun items)

let canAccessCrocomire items =
    canAccessHeatedNorfair items ||
        (canAccessKraid items &&
         canUsePowerBombs items &&
         haveItem items SpeedBooster &&
         (energyReserveCount items >= 2))

let canAccessLowerNorfair items = 
    canAccessHeatedNorfair items &&
    canUsePowerBombs items &&
    haveItem items Varia &&
        (haveItem items HiJump ||
         haveItem items Gravity)

let canPassWorstRoom items =
    canAccessLowerNorfair items &&
        (canFly items ||
         haveItem items Ice ||
         haveItem items HiJump)

let canAccessOuterMaridia items = 
    canAccessRedBrinstar items &&
    canUsePowerBombs items &&
        (haveItem items Gravity ||
         (haveItem items HiJump && haveItem items Ice))

let canAccessInnerMaridia items = 
    canAccessRedBrinstar items &&
    canUsePowerBombs items &&
    haveItem items Gravity

let canDoSuitlessMaridia items = 
     (haveItem items HiJump && haveItem items Ice && haveItem items Grapple)    

let canDefeatBotwoon items = 
    canAccessInnerMaridia items &&
    (haveItem items Ice || haveItem items SpeedBooster)

let canDefeatDraygon items = 
    canDefeatBotwoon items && haveItem items Gravity;

# Item Locations
let AllLocations = 
    [
        {
            Area = Crateria;
            Name = "Power Bomb (Crateria surface)";
            Class = Minor;
            Address = 0x781CC;
            Visibility = Visible;
            Available = fun items ->
                canUsePowerBombs items &&
                (haveItem items SpeedBooster || canFly items);
        };
        {
            Area = Crateria;
            Name = "Missile (outside Wrecked Ship bottom)";
            Class = Minor;
            Address = 0x781E8;
            Visibility = Visible;
            Available = fun items -> canAccessWs items;
        };
        {
            Area = Crateria;
            Name = "Missile (outside Wrecked Ship top)";
            Class = Minor;
            Address = 0x781EE;
            Visibility = Hidden;
            Available = fun items -> canAccessWs items;
        };
        {
            Area = Crateria;
            Name = "Missile (outside Wrecked Ship middle)";
            Class = Minor;
            Address = 0x781F4;
            Visibility = Visible;
            Available = fun items -> canAccessWs items;
        };
        {
            Area = Crateria;
            Name = "Missile (Crateria moat)";
            Class = Minor
            Address = 0x78248;
            Visibility = Visible;
            Available = fun items -> canAccessWs items;
        };
        {
            Area = Crateria;
            Name = "Energy Tank, Gauntlet";
            Class = Major;
            Address = 0x78264;
            Visibility = Visible;
            Available = fun items -> canEnterAndLeaveGauntlet items;
        };
        {
            Area = Crateria;
            Name = "Missile (Crateria bottom)";
            Class = Minor;
            Address = 0x783EE;
            Visibility = Visible;
            Available = fun items -> canDestroyBombWalls items;
        };
        {
            Area = Crateria;
            Name = "Bomb";
            Address = 0x78404;
            Class = Major;
            Visibility = Chozo;
            Available = fun items -> haveItem items Morph && canOpenRedDoors items;
        };
        {
            Area = Crateria;
            Name = "Energy Tank, Terminator";
            Class = Major;
            Address = 0x78432;
            Visibility = Visible;
            Available = fun items -> canDestroyBombWalls items || haveItem items SpeedBooster
        };
        {
            Area = Crateria;
            Name = "Missile (Crateria gauntlet right)";
            Class = Minor;
            Address = 0x78464;
            Visibility = Visible;
            Available = fun items -> canEnterAndLeaveGauntlet items && canPassBombPassages items;
        };
        {
            Area = Crateria;
            Name = "Missile (Crateria gauntlet left)";
            Class = Minor;
            Address = 0x7846A;
            Visibility = Visible;
            Available = fun items -> canEnterAndLeaveGauntlet items && canPassBombPassages items;
        };
        {
            Area = Crateria;
            Name = "Super Missile (Crateria)";
            Class = Minor;
            Address = 0x78478;                
            Visibility = Visible;
            Available = fun items -> canUsePowerBombs items && 
                                     haveItem items SpeedBooster && 
                                     (haveItem items ETank || haveItem items Varia || haveItem items Gravity)
        };
        {
            Area = Crateria;
            Name = "Missile (Crateria middle)";
            Class = Minor;
            Address = 0x78486;
            Visibility = Visible;
            Available = fun items -> canPassBombPassages items;
        };
        {
            Area = Brinstar;
            Name = "Power Bomb (green Brinstar bottom)";
            Class = Minor;
            Address = 0x784AC;
            Visibility = Chozo;
            Available = fun items -> canUsePowerBombs items;
        };
        {
            Area = Brinstar;
            Name = "Super Missile (pink Brinstar)";
            Class = Minor;
            Address = 0x784E4;
            Visibility = Chozo;
            Available = fun items -> canPassBombPassages items && haveItem items Super;
        };
        {
            Area = Brinstar;
            Name = "Missile (green Brinstar below super missile)";
            Class = Minor;
            Address = 0x78518;
            Visibility = Visible;
            Available = fun items -> canPassBombPassages items && canOpenRedDoors items;
        };
        {
            Area = Brinstar;
            Name = "Super Missile (green Brinstar top)";
            Class = Minor;
            Address = 0x7851E;
            Visibility = Visible;
            Available = fun items -> (haveItem items SpeedBooster || canDestroyBombWalls items) && canOpenRedDoors items && (haveItem items Morph || haveItem items SpeedBooster);
        };
        {
            Area = Brinstar;
            Name = "Reserve Tank, Brinstar";
            Class = Major;
            Address = 0x7852C;
            Visibility = Chozo;
            Available = fun items -> (haveItem items SpeedBooster || canDestroyBombWalls items) && canOpenRedDoors items && (haveItem items Morph || haveItem items SpeedBooster);
        };
        {
            Area = Brinstar;
            Name = "Missile (green Brinstar behind missile)";
            Class = Minor;
            Address = 0x78532;
            Visibility = Hidden;
            Available = fun items -> canPassBombPassages items && canOpenRedDoors items;
        };
        {
            Area = Brinstar;
            Name = "Missile (green Brinstar behind reserve tank)";
            Class = Minor;
            Address = 0x78538;
            Visibility = Visible;
            Available = fun items -> canDestroyBombWalls items && canOpenRedDoors items && haveItem items Morph;
        };
        {
            Area = Brinstar;
            Name = "Missile (pink Brinstar top)";
            Class = Minor;
            Address = 0x78608;
            Visibility = Visible;
            Available = fun items -> (canDestroyBombWalls items && canOpenRedDoors items) ||
                                     canUsePowerBombs items;
        };
        {
            Area = Brinstar;
            Name = "Missile (pink Brinstar bottom)";
            Class = Minor;
            Address = 0x7860E;
            Visibility = Visible;
            Available = fun items -> (canDestroyBombWalls items && canOpenRedDoors items) ||
                                     canUsePowerBombs items;
        };
        {
            Area = Brinstar;
            Name = "Charge Beam";
            Class = Major;
            Address = 0x78614;
            Visibility = Chozo;
            Available = fun items -> (canPassBombPassages items && canOpenRedDoors items) ||
                                     canUsePowerBombs items;
        };
        {
            Area = Brinstar;
            Name = "Power Bomb (pink Brinstar)";
            Class = Minor;
            Address = 0x7865C;
            Visibility = Visible;
            Available = fun items -> canUsePowerBombs items && haveItem items Super;
        };
        {
            Area = Brinstar;
            Name = "Missile (green Brinstar pipe)";
            Class = Minor;
            Address = 0x78676;
            Visibility = Visible;
            Available = fun items -> (canPassBombPassages items && canOpenGreenDoors items) || canUsePowerBombs items;
        };
        {
            Area = Brinstar;
            Name = "Morphing Ball";
            Class = Major;
            Address = 0x786DE;
            Visibility = Visible;
            Available = fun items -> true;
        };
        {
            Area = Brinstar;
            Name = "Power Bomb (blue Brinstar)";
            Class = Minor;
            Address = 0x7874C;
            Visibility = Visible;
            Available = fun items -> canUsePowerBombs items;
        };
        {
            Area = Brinstar;
            Name = "Missile (blue Brinstar middle)";
            Address = 0x78798;
            Class = Minor;
            Visibility = Visible;
            Available = fun items -> haveItem items Morph;
        };
        {
            Area = Brinstar;
            Name = "Energy Tank, Brinstar Ceiling";
            Class = Major;
            Address = 0x7879E;
            Visibility = Hidden;
            Available = fun items -> true;
        };
        {
            Area = Brinstar;
            Name = "Energy Tank, Etecoons";
            Class = Major;
            Address = 0x787C2;
            Visibility = Visible;
            Available = fun items -> canUsePowerBombs items;
        };
        {
            Area = Brinstar;
            Name = "Super Missile (green Brinstar bottom)";
            Class = Minor;
            Address = 0x787D0;
            Visibility = Visible;
            Available = fun items -> canUsePowerBombs items && canOpenGreenDoors items;
        };
        {
            Area = Brinstar;
            Name = "Energy Tank, Waterway";
            Class = Major;
            Address = 0x787FA;
            Visibility = Visible;
            Available = fun items -> canUsePowerBombs items && canOpenRedDoors items && haveItem items SpeedBooster;
        };
        {
            Area = Brinstar;
            Name = "Missile (blue Brinstar bottom)";
            Class = Minor;
            Address = 0x78802;
            Visibility = Chozo;
            Available = fun items -> haveItem items Morph;
        };
        {
            Area = Brinstar;
            Name = "Energy Tank, Brinstar Gate";
            Class = Major;
            Address = 0x78824;
            Visibility = Visible;
            Available = fun items -> canUsePowerBombs items &&
                                     (haveItem items Wave || (haveItem items Super && haveItem items HiJump));
        };
        {
            Area = Brinstar;
            Name = "Missile (blue Brinstar top)";
            Class = Minor;
            Address = 0x78836;
            Visibility = Visible;
            Available = fun items -> canUsePowerBombs items;
        };
        {
            Area = Brinstar;
            Name = "Missile (blue Brinstar behind missile)";
            Class = Minor;
            Address = 0x7883C;
            Visibility = Hidden;
            Available = fun items -> canUsePowerBombs items;
        };
        {
            Area = Brinstar;
            Name = "X-Ray Scope";
            Class = Major;
            Address = 0x78876;
            Visibility = Chozo;
            Available = fun items ->canAccessRedBrinstar items && 
                                    canUsePowerBombs items &&
                                    (haveItem items Grapple ||
                                     haveItem items SpaceJump ||
                                     (haveItem items Varia && energyReserveCount items >= 4) ||
                                     (energyReserveCount items >= 6))

        };
        {
            Area = Brinstar;
            Name = "Power Bomb (red Brinstar sidehopper room)";
            Class = Minor;
            Address = 0x788CA;
            Visibility = Visible;
            Available = fun items -> canAccessRedBrinstar items && canUsePowerBombs items;
        };
        {
            Area = Brinstar;
            Name = "Power Bomb (red Brinstar spike room)";
            Class = Minor;
            Address = 0x7890E;
            Visibility = Chozo;
            Available = fun items -> canAccessRedBrinstar items && canUsePowerBombs items;
        };
        {
            Area = Brinstar;
            Name = "Missile (red Brinstar spike room)";
            Class = Minor;
            Address = 0x78914;
            Visibility = Visible;
            Available = fun items -> canAccessRedBrinstar items && canUsePowerBombs items;
        };
        {
            Area = Brinstar;
            Name = "Spazer";
            Class = Major;
            Address = 0x7896E;
            Visibility = Chozo;
            Available = fun items -> canAccessRedBrinstar items;
        };
        {
            Area = Brinstar;
            Name = "Energy Tank, Kraid";
            Class = Major;
            Address = 0x7899C;
            Visibility = Hidden;
            Available = fun items -> canAccessKraid items;
        };
        {
            Area = Brinstar;
            Name = "Missile (Kraid)";
            Class = Minor;
            Address = 0x789EC;
            Visibility = Hidden;
            Available = fun items -> canAccessKraid items && canUsePowerBombs items;
        };
        {
            Area = Brinstar;
            Name = "Varia Suit";
            Class = Major;
            Address = 0x78ACA;
            Visibility = Chozo;
            Available = fun items -> canAccessKraid items;
        };
        {
            Area = Norfair;
            Name = "Missile (lava room)";
            Class = Minor;
            Address = 0x78AE4;
            Visibility = Hidden;
            Available = fun items -> canAccessHeatedNorfair items;
        };
        {
            Area = Norfair;
            Name = "Ice Beam";
            Class = Major;
            Address = 0x78B24;
            Visibility = Chozo;
            Available = fun items -> canAccessKraid items &&
                                     (heatProof items || energyReserveCount items >= 2);
        };
        {
            Area = Norfair;
            Name = "Missile (below Ice Beam)";
            Class = Minor;
            Address = 0x78B46;
            Visibility = Hidden;
            Available = fun items -> canAccessKraid items && 
                                     canUsePowerBombs items && 
                                     canHellRun items;                                         
        };
        {
            Area = Norfair;
            Name = "Energy Tank, Crocomire";
            Class = Major;
            Address = 0x78BA4;
            Visibility = Visible;
            Available = fun items -> canAccessCrocomire items;
        };
        {
            Area = Norfair;
            Name = "Hi-Jump Boots";
            Class = Major;
            Address = 0x78BAC;
            Visibility = Chozo;
            Available = fun items -> canAccessRedBrinstar items;
        };
        {
            Area = Norfair;
            Name = "Missile (above Crocomire)";
            Class = Minor;
            Address = 0x78BC0;
            Visibility = Visible;
            Available = fun items -> canAccessCrocomire items &&
                                        (canFly items || 
                                         haveItem items Grapple ||
                                         (haveItem items HiJump && haveItem items SpeedBooster))
        };
        {
            Area = Norfair;
            Name = "Missile (Hi-Jump Boots)";
            Class = Minor;
            Address = 0x78BE6;
            Visibility = Visible;
            Available = fun items -> canAccessRedBrinstar items;
        };
        {
            Area = Norfair;
            Name = "Energy Tank (Hi-Jump Boots)";
            Class = Minor;
            Address = 0x78BEC;
            Visibility = Visible;
            Available = fun items -> canAccessRedBrinstar items;
        };
        {
            Area = Norfair;
            Name = "Power Bomb (Crocomire)";
            Class = Minor;
            Address = 0x78C04;
            Visibility = Visible;
            Available = fun items -> canAccessCrocomire items;
        };
        {
            Area = Norfair;
            Name = "Missile (below Crocomire)";
            Class = Minor;
            Address = 0x78C14;
            Visibility = Visible;
            Available = fun items -> canAccessCrocomire items;
        };
        {
            Area = Norfair;
            Name = "Missile (Grapple Beam)";
            Class = Minor;
            Address = 0x78C2A;
            Visibility = Visible;
            Available = fun items -> canAccessCrocomire items &&
                                        (canFly items ||
                                         haveItem items Grapple ||
                                         haveItem items SpeedBooster);
        };
        {
            Area = Norfair;
            Name = "Grapple Beam";
            Class = Major;
            Address = 0x78C36;
            Visibility = Chozo;
            Available = fun items -> canAccessCrocomire items &&
                                        (canFly items ||
                                         haveItem items Ice ||
                                         haveItem items SpeedBooster);
        };
        {
            Area = Norfair;
            Name = "Reserve Tank, Norfair";
            Class = Major;
            Address = 0x78C3E;
            Visibility = Chozo;
            Available = fun items -> canAccessHeatedNorfair items &&
                                        (canFly items ||
                                         haveItem items Grapple ||
                                         haveItem items HiJump);
        };
        {
            Area = Norfair;
            Name = "Missile (Norfair Reserve Tank)";
            Class = Minor;
            Address = 0x78C44;
            Visibility = Hidden;
            Available = fun items -> canAccessHeatedNorfair items &&
                                        (canFly items ||
                                         haveItem items Grapple ||
                                         haveItem items HiJump);
        };
        {
            Area = Norfair;
            Name = "Missile (bubble Norfair green door)";
            Class = Minor;
            Address = 0x78C52;
            Visibility = Visible;
            Available = fun items -> canAccessHeatedNorfair items &&
                                        (canFly items ||
                                         haveItem items Grapple ||
                                         haveItem items HiJump);
        };
        {
            Area = Norfair;
            Name = "Missile (bubble Norfair)";
            Class = Minor;
            Address = 0x78C66;
            Visibility = Visible;
            Available = fun items -> canAccessHeatedNorfair items;
        };
        {
            Area = Norfair;
            Name = "Missile (Speed Booster)";
            Class = Minor;
            Address = 0x78C74;
            Visibility = Hidden;
            Available = fun items -> canAccessHeatedNorfair items;
        };
        {
            Area = Norfair;
            Name = "Speed Booster";
            Class = Major;
            Address = 0x78C82;
            Visibility = Chozo;
            Available = fun items -> canAccessHeatedNorfair items;
        };
        {
            Area = Norfair;
            Name = "Missile (Wave Beam)";
            Class = Minor;
            Address = 0x78CBC;
            Visibility = Visible;
            Available = fun items -> canAccessHeatedNorfair items;
        };
        {
            Area = Norfair;
            Name = "Wave Beam";
            Class = Major;
            Address = 0x78CCA;
            Visibility = Chozo;
            Available = fun items -> canAccessHeatedNorfair items;
        };
        {
            Area = LowerNorfair;
            Name = "Missile (Gold Torizo)";
            Class = Minor;
            Address = 0x78E6E;
            Visibility = Visible;
            Available = fun items -> canAccessLowerNorfair items && haveItem items SpaceJump;
        };
        {
            Area = LowerNorfair;
            Name = "Super Missile (Gold Torizo)";
            Class = Minor;
            Address = 0x78E74;
            Visibility = Hidden;
            Available = fun items -> canAccessLowerNorfair items;
        };
        {
            Area = LowerNorfair;
            Name = "Missile (Mickey Mouse room)";
            Class = Minor;
            Address = 0x78F30;
            Visibility = Visible;
            Available = fun items -> canPassWorstRoom items;
        };
        {
            Area = LowerNorfair;
            Name = "Missile (lower Norfair above fire flea room)";
            Class = Minor;
            Address = 0x78FCA;
            Visibility = Visible;
            Available = fun items -> canPassWorstRoom items;
        };
        {
            Area = LowerNorfair;
            Name = "Power Bomb (lower Norfair above fire flea room)";
            Class = Minor;
            Address = 0x78FD2;
            Visibility = Visible;
            Available = fun items -> canPassWorstRoom items;
        };
        {
            Area = LowerNorfair;
            Name = "Power Bomb (Power Bombs of shame)";
            Class = Minor;
            Address = 0x790C0;
            Visibility = Visible;
            Available = fun items -> canPassWorstRoom items;
        };
        {
            Area = LowerNorfair;
            Name = "Missile (lower Norfair near Wave Beam)";
            Class = Minor;
            Address = 0x79100;
            Visibility = Visible;
            Available = fun items -> canPassWorstRoom items;
        };
        {
            Area = LowerNorfair;
            Name = "Energy Tank, Ridley";
            Class = Major;
            Address = 0x79108;
            Visibility = Hidden;
            Available = fun items -> canPassWorstRoom items;
        };
        {
            Area = LowerNorfair;
            Name = "Screw Attack";
            Class = Major;
            Address = 0x79110;
            Visibility = Chozo;
            Available = fun items -> canAccessLowerNorfair items;
        };
        {
            Area = LowerNorfair;
            Name = "Energy Tank, Firefleas";
            Class = Major;
            Address = 0x79184;
            Visibility = Visible;
            Available = fun items -> canPassWorstRoom items;
        };
        {
            Area = WreckedShip;
            Name = "Missile (Wrecked Ship middle)";
            Class = Minor;
            Address = 0x7C265;
            Visibility = Visible;
            Available = fun items -> canAccessWs items;
        };
        {
            Area = WreckedShip;
            Name = "Reserve Tank, Wrecked Ship";
            Class = Major;
            Address = 0x7C2E9;
            Visibility = Chozo;
            Available = fun items -> canAccessWs items &&
                                     haveItem items SpeedBooster &&
                                     (haveItem items Varia || energyReserveCount items >= 1);
        };
        {
            Area = WreckedShip;
            Name = "Missile (Gravity Suit)";
            Class = Minor;
            Address = 0x7C2EF;
            Visibility = Visible;
            Available = fun items -> canAccessWs items &&
                                     (haveItem items Varia || energyReserveCount items >= 1);
        };
        {
            Area = WreckedShip;
            Name = "Missile (Wrecked Ship top)";
            Class = Minor;
            Address = 0x7C319;
            Visibility = Visible;
            Available = fun items -> canAccessWs items;
        };
        {
            Area = WreckedShip;
            Name = "Energy Tank, Wrecked Ship";
            Class = Major;
            Address = 0x7C337;
            Visibility = Visible;
            Available = fun items -> canAccessWs items &&
                                        (haveItem items Bomb ||
                                         haveItem items PowerBomb ||
                                         haveItem items HiJump ||
                                         haveItem items SpaceJump ||
                                         haveItem items SpeedBooster ||
                                         haveItem items SpringBall);
        };
        {
            Area = WreckedShip;
            Name = "Super Missile (Wrecked Ship left)";
            Class = Minor;
            Address = 0x7C357;
            Visibility = Visible;
            Available = fun items -> canAccessWs items;
        };
        {
            Area = WreckedShip;
            Name = "Right Super, Wrecked Ship";
            Class = Major;
            Address = 0x7C365;
            Visibility = Visible;
            Available = fun items -> canAccessWs items;
        };
        {
            Area = WreckedShip;
            Name = "Gravity Suit";
            Class = Major;
            Address = 0x7C36D;
            Visibility = Chozo;
            Available = fun items -> canAccessWs items &&
                                     (haveItem items Varia || energyReserveCount items >= 1);
        };
        {
            Area = Maridia;
            Name = "Missile (green Maridia shinespark)";
            Class = Minor;
            Address = 0x7C437;
            Visibility = Visible;
            Available = fun items -> canAccessRedBrinstar items &&
                                     canUsePowerBombs items &&
                                     haveItem items Gravity &&
                                     haveItem items SpeedBooster;
        };
        {
            Area = Maridia;
            Name = "Super Missile (green Maridia)";
            Class = Minor;
            Address = 0x7C43D;
            Visibility = Visible;
            Available = fun items -> canAccessOuterMaridia items;
        };
        {
            Area = Maridia;
            Name = "Energy Tank, Mama turtle";
            Class = Major;
            Address = 0x7C47D;
            Visibility = Visible;
            Available = fun items -> canAccessOuterMaridia items &&
                                        (canFly items ||
                                         haveItem items SpeedBooster ||
                                         haveItem items Grapple);
        };
        {
            Area = Maridia;
            Name = "Missile (green Maridia tatori)";
            Class = Minor;
            Address = 0x7C483;
            Visibility = Hidden;
            Available = fun items -> canAccessOuterMaridia items;
        };
        {
            Area = Maridia;
            Name = "Super Missile (yellow Maridia)";
            Class = Minor;
            Address = 0x7C4AF;
            Visibility = Visible;
            Available = fun items -> canAccessInnerMaridia items;
        };
        {
            Area = Maridia;
            Name = "Missile (yellow Maridia super missile)";
            Class = Minor;
            Address = 0x7C4B5;
            Visibility = Visible;
            Available = fun items -> canAccessInnerMaridia items;
        };
        {
            Area = Maridia;
            Name = "Missile (yellow Maridia false wall)";
            Class = Minor;
            Address = 0x7C533;
            Visibility = Visible;
            Available = fun items -> canAccessInnerMaridia items;
        };
        {
            Area = Maridia;
            Name = "Plasma Beam";
            Class = Major;
            Address = 0x7C559;
            Visibility = Chozo;
            Available = fun items -> canDefeatDraygon items &&
                                     (haveItem items SpeedBooster ||
                                        (haveItem items Charge ||
                                         haveItem items ScrewAttack) &&
                                        (canFly items || haveItem items HiJump));
        };
        {
            Area = Maridia;
            Name = "Missile (left Maridia sand pit room)";
            Class = Minor;
            Address = 0x7C5DD;
            Visibility = Visible;
            Available = fun items -> canAccessInnerMaridia items;
        };
        {
            Area = Maridia;
            Name = "Reserve Tank, Maridia";
            Class = Major;
            Address = 0x7C5E3;
            Visibility = Chozo;
            Available = fun items -> (canAccessOuterMaridia items && (canDoSuitlessMaridia items || haveItem items Gravity));
        };
        {
            Area = Maridia;
            Name = "Missile (right Maridia sand pit room)";
            Class = Minor;
            Address = 0x7C5EB;
            Visibility = Visible;
            Available = fun items -> canAccessInnerMaridia items;
        };
        {
            Area = Maridia;
            Name = "Power Bomb (right Maridia sand pit room)";
            Class = Minor;
            Address = 0x7C5F1;
            Visibility = Visible;
            Available = fun items -> canAccessOuterMaridia items &&
                                     haveItem items Gravity;
        };
        {
            Area = Maridia;
            Name = "Missile (pink Maridia)";
            Address = 0x7C603;
            Class = Minor;
            Visibility = Visible;
            Available = fun items -> canAccessOuterMaridia items &&
                                     haveItem items Gravity;
        };
        {
            Area = Maridia;
            Name = "Super Missile (pink Maridia)";
            Class = Minor;
            Address = 0x7C609;
            Visibility = Visible;
            Available = fun items -> canAccessOuterMaridia items &&
                                     haveItem items Gravity;
        };
        {
            Area = Maridia;
            Name = "Spring Ball";
            Class = Major;
            Address = 0x7C6E5;
            Visibility = Chozo;
            Available = fun items -> canAccessInnerMaridia items &&                                         
                                     (haveItem items Ice || (haveItem items Grapple && (canFly items || haveItem items HiJump)));
        };
        {
            Area = Maridia;
            Name = "Missile (Draygon)";
            Class = Minor;
            Address = 0x7C74D;
            Visibility = Hidden;
            Available = fun items -> canDefeatBotwoon items;
        };
        {
            Area = Maridia;
            Name = "Energy Tank, Botwoon";
            Class = Major;
            Address = 0x7C755;
            Visibility = Visible;
            Available = fun items -> canDefeatBotwoon items ||
                                     (canAccessOuterMaridia items && canDoSuitlessMaridia items);
        };
        {
            Area = Maridia;
            Name = "Space Jump";
            Class = Major;
            Address = 0x7C7A7;
            Visibility = Chozo;
            Available = fun items -> canDefeatDraygon items;
        }
    ];
