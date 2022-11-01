-- store statistics about item placements

create table if not exists extended_stats (
  -- uniq identifier for join with item_locs
  id int unsigned not null auto_increment,
  -- skill preset
  randoPreset varchar(32),
  -- randomizer preset
  skillPreset varchar(32),

  -- how many seeds
  count int unsigned default 0,
  primary key(randoPreset, skillPreset),
  index(id)
);
-- alter table extended_stats drop version;

create table if not exists item_locs (
  -- to join with extend_stats
  ext_id int unsigned not null,
  -- item
  item varchar(16) not null,
  -- locations (count how time the item has been placed at each location)
  EnergyTankGauntlet  int unsigned default 0,
  Bomb  int unsigned default 0,
  EnergyTankTerminator  int unsigned default 0,
  ReserveTankBrinstar  int unsigned default 0,
  ChargeBeam  int unsigned default 0,
  MorphingBall  int unsigned default 0,
  EnergyTankBrinstarCeiling  int unsigned default 0,
  EnergyTankEtecoons  int unsigned default 0,
  EnergyTankWaterway  int unsigned default 0,
  EnergyTankBrinstarGate  int unsigned default 0,
  XRayScope  int unsigned default 0,
  Spazer  int unsigned default 0,
  EnergyTankKraid  int unsigned default 0,
  Kraid  int unsigned default 0,
  VariaSuit  int unsigned default 0,
  IceBeam  int unsigned default 0,
  EnergyTankCrocomire  int unsigned default 0,
  HiJumpBoots  int unsigned default 0,
  GrappleBeam  int unsigned default 0,
  ReserveTankNorfair  int unsigned default 0,
  SpeedBooster  int unsigned default 0,
  WaveBeam  int unsigned default 0,
  Ridley  int unsigned default 0,
  EnergyTankRidley  int unsigned default 0,
  ScrewAttack  int unsigned default 0,
  EnergyTankFirefleas  int unsigned default 0,
  ReserveTankWreckedShip  int unsigned default 0,
  EnergyTankWreckedShip  int unsigned default 0,
  Phantoon  int unsigned default 0,
  RightSuperWreckedShip  int unsigned default 0,
  GravitySuit  int unsigned default 0,
  EnergyTankMamaturtle  int unsigned default 0,
  PlasmaBeam  int unsigned default 0,
  ReserveTankMaridia  int unsigned default 0,
  SpringBall  int unsigned default 0,
  EnergyTankBotwoon  int unsigned default 0,
  Draygon  int unsigned default 0,
  SpaceJump  int unsigned default 0,
  MotherBrain  int unsigned default 0,
  SporeSpawn  int unsigned default 0,
  Botwoon  int unsigned default 0,
  Crocomire  int unsigned default 0,
  GoldenTorizo  int unsigned default 0,
  PowerBombCrateriasurface  int unsigned default 0,
  MissileoutsideWreckedShipbottom  int unsigned default 0,
  MissileoutsideWreckedShiptop  int unsigned default 0,
  MissileoutsideWreckedShipmiddle  int unsigned default 0,
  MissileCrateriamoat  int unsigned default 0,
  MissileCrateriabottom  int unsigned default 0,
  MissileCrateriagauntletright  int unsigned default 0,
  MissileCrateriagauntletleft  int unsigned default 0,
  SuperMissileCrateria  int unsigned default 0,
  MissileCrateriamiddle  int unsigned default 0,
  PowerBombgreenBrinstarbottom  int unsigned default 0,
  SuperMissilepinkBrinstar  int unsigned default 0,
  MissilegreenBrinstarbelowsupermissile  int unsigned default 0,
  SuperMissilegreenBrinstartop  int unsigned default 0,
  MissilegreenBrinstarbehindmissile  int unsigned default 0,
  MissilegreenBrinstarbehindreservetank  int unsigned default 0,
  MissilepinkBrinstartop  int unsigned default 0,
  MissilepinkBrinstarbottom  int unsigned default 0,
  PowerBombpinkBrinstar  int unsigned default 0,
  MissilegreenBrinstarpipe  int unsigned default 0,
  PowerBombblueBrinstar  int unsigned default 0,
  MissileblueBrinstarmiddle  int unsigned default 0,
  SuperMissilegreenBrinstarbottom  int unsigned default 0,
  MissileblueBrinstarbottom  int unsigned default 0,
  MissileblueBrinstartop  int unsigned default 0,
  MissileblueBrinstarbehindmissile  int unsigned default 0,
  PowerBombredBrinstarsidehopperroom  int unsigned default 0,
  PowerBombredBrinstarspikeroom  int unsigned default 0,
  MissileredBrinstarspikeroom  int unsigned default 0,
  MissileKraid  int unsigned default 0,
  Missilelavaroom  int unsigned default 0,
  MissilebelowIceBeam  int unsigned default 0,
  MissileaboveCrocomire  int unsigned default 0,
  MissileHiJumpBoots  int unsigned default 0,
  EnergyTankHiJumpBoots  int unsigned default 0,
  PowerBombCrocomire  int unsigned default 0,
  MissilebelowCrocomire  int unsigned default 0,
  MissileGrappleBeam  int unsigned default 0,
  MissileNorfairReserveTank  int unsigned default 0,
  MissilebubbleNorfairgreendoor  int unsigned default 0,
  MissilebubbleNorfair  int unsigned default 0,
  MissileSpeedBooster  int unsigned default 0,
  MissileWaveBeam  int unsigned default 0,
  MissileGoldTorizo  int unsigned default 0,
  SuperMissileGoldTorizo  int unsigned default 0,
  MissileMickeyMouseroom  int unsigned default 0,
  MissilelowerNorfairabovefireflearoom  int unsigned default 0,
  PowerBomblowerNorfairabovefireflearoom  int unsigned default 0,
  PowerBombPowerBombsofshame  int unsigned default 0,
  MissilelowerNorfairnearWaveBeam  int unsigned default 0,
  MissileWreckedShipmiddle  int unsigned default 0,
  MissileGravitySuit  int unsigned default 0,
  MissileWreckedShiptop  int unsigned default 0,
  SuperMissileWreckedShipleft  int unsigned default 0,
  MissilegreenMaridiashinespark  int unsigned default 0,
  SuperMissilegreenMaridia  int unsigned default 0,
  MissilegreenMaridiatatori  int unsigned default 0,
  SuperMissileyellowMaridia  int unsigned default 0,
  MissileyellowMaridiasupermissile  int unsigned default 0,
  MissileyellowMaridiafalsewall  int unsigned default 0,
  MissileleftMaridiasandpitroom  int unsigned default 0,
  MissilerightMaridiasandpitroom  int unsigned default 0,
  PowerBombrightMaridiasandpitroom  int unsigned default 0,
  MissilepinkMaridia  int unsigned default 0,
  SuperMissilepinkMaridia  int unsigned default 0,
  MissileDraygon  int unsigned default 0,
  primary key(ext_id, item)
);

create table if not exists techniques (
  -- to join with extend_stats
  ext_id int unsigned not null,
  -- technique (count how many times the technique has been used)
  technique varchar(64) not null,
  count int unsigned default 0,
  primary key(ext_id, technique)
);

create table if not exists difficulties (
  -- to join with extend_stats
  ext_id int unsigned not null,
  -- count each difficulty to make an histogram
  easy int unsigned default 0,
  medium int unsigned default 0,
  hard int unsigned default 0,
  harder int unsigned default 0,
  hardcore int unsigned default 0,
  mania int unsigned default 0,
  primary key(ext_id)
);

create table if not exists solver_stats (
  -- to join with extend_stats
  ext_id int unsigned not null,
  name varchar(8) not null,
  value int unsigned default 0
);
create index solver_stats_idx01 on solver_stats(ext_id, name);
