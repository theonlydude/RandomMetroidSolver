# RandomMetroidSolver
Check a randomized super metroid rom and display its estimated difficulty

There's a website to use the solver: [Super Metroid Item Randomizer Solver](http://randommetroidsolver.pythonanywhere.com/)


Or in command line:
```sh
usage: solver.py [-h] [--param PARAMSFILENAME [PARAMSFILENAME ...]] [--debug]
                 [--difficultyTarget [DIFFICULTYTARGET]]
                 [--displayGeneratedPath]
                 romFileName
```

Example:
```
dude@dude-ordi ~/RandomMetroidSolver $ ./solver.py tests/roms/Item\ Randomizer\ TX3919157.json -g
Generated path:
                                     Location Name:         Area             Item Difficulty
--------------------------------------------------------------------------------------------
                                     Morphing Ball:     Brinstar        SpaceJump 0
                     Energy Tank, Brinstar Ceiling:     Brinstar            Morph 1
                    Missile (blue Brinstar middle):     Brinstar            Super 0
                    Missile (blue Brinstar bottom):     Brinstar          Missile 0
                                              Bomb:     Crateria      ScrewAttack 25
                           Energy Tank, Terminator:     Crateria     SpeedBooster 0
                             Energy Tank, Gauntlet:     Crateria           HiJump 0
                           Missile (Crateria moat):     Crateria          Missile 0
                         Missile (Crateria bottom):     Crateria            Super 0
                            Reserve Tank, Brinstar:     Brinstar            ETank 0
                                            Spazer:     Brinstar             Bomb 0
                                       Charge Beam:     Brinstar            ETank 0
                                        Varia Suit:     Brinstar            Varia 1.5015015015
                                Energy Tank, Kraid:     Brinstar           Plasma 0
                     Super Missile (pink Brinstar):     Brinstar          Missile 0
      Missile (green Brinstar below super missile):     Brinstar            Super 0
                Super Missile (green Brinstar top):     Brinstar          Missile 0
           Missile (green Brinstar behind missile):     Brinstar          Missile 0
      Missile (green Brinstar behind reserve tank):     Brinstar            Super 0
                       Missile (pink Brinstar top):     Brinstar        PowerBomb 0
                             Energy Tank, Etecoons:     Brinstar            ETank 0
                                       X-Ray Scope:     Brinstar          Reserve 0
                Power Bomb (green Brinstar bottom):     Brinstar            Super 0
                    Missile (pink Brinstar bottom):     Brinstar            Super 0
                        Power Bomb (pink Brinstar):     Brinstar            Super 0
                     Missile (green Brinstar pipe):     Brinstar            Super 0
                        Power Bomb (blue Brinstar):     Brinstar            Super 0
             Super Missile (green Brinstar bottom):     Brinstar            Super 0
                       Missile (blue Brinstar top):     Brinstar            Super 0
            Missile (blue Brinstar behind missile):     Brinstar        PowerBomb 0
         Power Bomb (red Brinstar sidehopper room):     Brinstar            Super 0
              Power Bomb (red Brinstar spike room):     Brinstar            Super 0
                 Missile (red Brinstar spike room):     Brinstar          Missile 0
                                   Missile (Kraid):     Brinstar          Missile 0
                                          Ice Beam:      Norfair           Charge 0
                            Energy Tank, Crocomire:      Norfair          Reserve 0
                                     Hi-Jump Boots:      Norfair          Gravity 0
                                      Grapple Beam:      Norfair            ETank 0
                                     Speed Booster:      Norfair        XRayScope 1
                                         Wave Beam:      Norfair            ETank 1
                             Reserve Tank, Norfair:      Norfair            ETank 2
                         Missile (above Crocomire):      Norfair            Super 0
                           Missile (Hi-Jump Boots):      Norfair            Super 0
                       Energy Tank (Hi-Jump Boots):      Norfair          Missile 0
                            Power Bomb (Crocomire):      Norfair            Super 0
                         Missile (below Crocomire):      Norfair            Super 0
                            Missile (Grapple Beam):      Norfair            Super 0
                               Missile (lava room):      Norfair            Super 1
                          Missile (below Ice Beam):      Norfair          Missile 1
                          Missile (bubble Norfair):      Norfair          Missile 1
                           Missile (Speed Booster):      Norfair            Super 1
                               Missile (Wave Beam):      Norfair          Missile 1
                    Missile (Norfair Reserve Tank):      Norfair            Super 2
               Missile (bubble Norfair green door):      Norfair          Missile 2
                                      Screw Attack: LowerNorfair          Grapple 0
                            Energy Tank, Firefleas: LowerNorfair       SpringBall 1
                             Missile (Gold Torizo): LowerNorfair            Super 0
                       Super Missile (Gold Torizo): LowerNorfair          Missile 0
                       Missile (Mickey Mouse room): LowerNorfair          Missile 1
      Missile (lower Norfair above fire flea room): LowerNorfair            Super 1
   Power Bomb (lower Norfair above fire flea room): LowerNorfair          Missile 1
                 Power Bomb (Power Bombs of shame): LowerNorfair          Missile 1
            Missile (lower Norfair near Wave Beam): LowerNorfair            Super 1
                          Energy Tank, Mama turtle:      Maridia              Ice 0
                             Reserve Tank, Maridia:      Maridia            ETank 0
                                       Spring Ball:      Maridia            ETank 0
                              Energy Tank, Botwoon:      Maridia            ETank 0
                                        Space Jump:      Maridia          Reserve 1
                             Energy Tank, Waterway:     Brinstar            ETank 0
                         Right Super, Wrecked Ship:  WreckedShip            ETank 0.782032032032
                        Reserve Tank, Wrecked Ship:  WreckedShip           Spazer 0
                         Energy Tank, Wrecked Ship:  WreckedShip            ETank 0
                                      Gravity Suit:  WreckedShip             Wave 0
                        Energy Tank, Brinstar Gate:     Brinstar            ETank 0
                                       Plasma Beam:      Maridia            ETank 2
                               Energy Tank, Ridley: LowerNorfair          Reserve 5.5045045045
                                           The End:      The End          The End 0.518518518519
Estimated difficulty: very hard ^------------------------- hardcore
```
