# VARIA Randomizer, Solver, Tracker, Plandomizer for Super Metroid

There's a website to use the VARIA Randomizer, Solver, Tracker, Plandomizer: [http://varia.run/](http://varia.run/)

The current work in progress version is available on the beta website [http://beta.varia.run/](http://beta.varia.run/)

You can join the VARIA discord too: [http://discord.varia.run/](http://discord.varia.run/)

# Getting the sources

You need a git client:
```
dude@computer:~$ git clone git@github.com:theonlydude/RandomMetroidSolver.git
dude@computer:~$ cd RandomMetroidSolver
```

The current work in progress version is in the master branch (the default one, accessible on beta website (http://beta.varia.run/), if you want the version running on the production website (http://varia.run/) you have to checkout the production branch:
```
dude@computer:~/RandomMetroidSolver (master)$ git checkout production
Basculement sur la branche 'production'
Votre branche est à jour avec 'origin/production'.
dude@computer:~/RandomMetroidSolver (production)$ 
```

# CLI Randomizer

You need Python >= 3.6, it has been tested on Linux and CYGWIN.

As VARIA Randomizer has a lot of options, the easiest way to use it is with a Randomizer preset (--randoPreset), you also need a skill preset to tell the Randomizer which tricks he can use to acces the locations (--param) and a vanilla ROM (-r), you can optionally give a seed number (--seed), if not a random one is chosen:

```
dude@computer:~/RandomMetroidSolver (master)$ python3.7 ./randomizer.py -r ~/metroid/SuperMetroid.sfc --param standard_presets/Season_Races.json --randoPreset rando_presets/default.json --seed 1097821
```

You can start with an existing Randomizer preset and create a temporary one to update the parameters you want to change in the json, you can also set the parameters by hand but there's many many parameters (see web/controllers/solver_web.py for the call to randomizer.py using parameters)

To list all the Randomizer parameters and their description:
```
dude@computer:~/RandomMetroidSolver (master)$ python3.7 ./randomizer.py -h
  --param PARAMSFILENAME [PARAMSFILENAME ...], -p PARAMSFILENAME [PARAMSFILENAME ...]
                        the input parameters
  --seed [SEED], -s [SEED]
                        randomization seed to use
  --rom [ROM], -r [ROM]
                        the vanilla ROM
  --randoPreset [RANDOPRESET]
                        rando preset file
```

# CLI Solver

There's less options for the Solver, it needs a seed (-r), a skill preset (--preset) and optionally a difficulty limit (--difficultyTarget) and a pickup stragegy (--pickupStrategy). You can display the spoiler log with -g.

```
dude@computer:~/RandomMetroidSolver (master)$ python3.7 ./solver.py -r VARIA_Randomizer_FX1097821_Season_Races_medium.sfc  --preset standard_presets/Season_Races.json --difficultyTarget 10 --pickupStrategy all -g
```

The difficulty values:
```
easy = 1
medium = 5
hard = 10
harder = 25
hardcore = 50
mania = 100
```

see web/controllers/solver_web.py for the call to solver.py using parameters.

To list all the Solver parameters and their description:
```
dude@computer:~/RandomMetroidSolver (master)$ python3.7 ./solver.py -h
  --romFileName [ROMFILENAME], -r [ROMFILENAME]
                        the input rom
  --preset [PRESETFILENAME], -p [PRESETFILENAME]
                        the preset file
  --difficultyTarget [DIFFICULTYTARGET], -t [DIFFICULTYTARGET]
                        the difficulty target that the solver will aim for
  --pickupStrategy [{minimal,all,any}], -s [{minimal,all,any}]
                        Pickup strategy for the Solver
  --displayGeneratedPath, -g
                        display the generated path (spoilers!)
```

# CLI Randomizer webservice client

You can call a VARIA website to generate your seed (a local one, beta or production) using the webservice client, it can be used for example on a Raspberry Pi with limited CPU power.

```
dude@computer:~/RandomMetroidSolver (master)$ python3.7 ./randomizer_webservice.py --rom ~/metroid/SuperMetroid.sfc --skillPreset standard_presets/Season_Races.json --randoPreset rando_presets/where_am_i.json --seed 1356988 --remoteUrl beta

VARIA_Randomizer_AFX1356988_Season_Races_VARIAble.sfc generated succesfully
```

To list all theRandomizer webservice client parameters and their description:
```
dude@computer:~/RandomMetroidSolver (master)$ python3.7 randomizer_webservice.py 
  --skillPreset [SKILLPRESET]
                        skill preset file
  --rom [ROM]           vanilla ROM file
  --randoPreset [RANDOPRESET]
                        rando preset file
  --seed [SEED]         seed number (optional)
  --remoteUrl [{local,beta,production}]
                        remote url to connect to
```