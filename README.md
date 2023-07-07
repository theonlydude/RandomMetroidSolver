# VARIA Randomizer, Solver, Tracker, Plandomizer for Super Metroid

There's a website to use the VARIA Randomizer, Solver, Tracker, Plandomizer: [http://varia.run/](http://varia.run/)

The current work in progress version is available on the beta website [http://beta.varia.run/](http://beta.varia.run/)

You can join the VARIA discord too: [http://discord.varia.run/](http://discord.varia.run/)

# Getting the sources

You need a git client:
```
dude@computer:~$ git clone --recurse-submodules git@github.com:theonlydude/RandomMetroidSolver.git
dude@computer:~$ cd RandomMetroidSolver
dude@computer:~/RandomMetroidSolver (master)$ git submodule foreach git checkout main
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

As VARIA Randomizer has a lot of options, the only supported way of using it is with a Randomizer preset (--randoPreset), you also need a skill preset to tell the Randomizer which tricks he can use to acces the locations (--param) and a vanilla ROM (-r), you can optionally give a seed number (--seed), if not a random one is chosen:

```
dude@computer:~/RandomMetroidSolver (master)$ python3.7 ./randomizer.py -r ~/metroid/SuperMetroid.sfc --param standard_presets/Season_Races.json --randoPreset rando_presets/default.json --seed 1097821
```

You can start with an existing Randomizer preset and create a temporary one to update the parameters you want to change in the json, you can also set the parameters by hand but there's many many parameters (see web/controllers/solver_web.py for the call to randomizer.py using parameters)

For startLocation, majorsSplit, progressionSpeed, progressionDifficulty, morphPlacement and energyQty if you set them to random you can add a second parameter to give the list of possible values (see haste Randomizer preset for an example).

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

To list all the Randomizer webservice client parameters and their description:
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

# CLI Customizer

To change Samus sprite or apply patches or randomize palettes on an existing seed you have to call the Customizer. It'll generate a new ROM prefixed with: Custom_

To add a sprite use --sprite, the available sprites are in varia_custom_sprites submodule.

To add one or more patches use --patch, the available patches are available in customizer.py.

Example:
```
dude@computer:~/RandomMetroidSolver (master)$ python3.7 ./customizer.py -r VARIA_Randomizer_FX1097821_Season_Races_medium.sfc --sprite megaman --patch itemsounds.ips --patch No_Music
Apply patch itemsounds.ips
Apply patch No_Music
Apply patch megaman.ips
Customzied Rom generated: Custom_VARIA_Randomizer_FX1097821_Season_Races_medium.sfc
```

To add colors randomization:

The parameters:
```
  --palette             Randomize the palettes
  --individual_suit_shift
  --individual_tileset_shift
  --no_match_ship_and_power
  --seperate_enemy_palette_groups
  --no_match_room_shift_with_boss
  --no_shift_tileset_palette
  --no_shift_boss_palettes
  --no_shift_suit_palettes
  --no_shift_enemy_palettes
  --no_shift_beam_palettes
  --no_shift_ship_palette
  --min_degree [MIN_DEGREE]
  --max_degree [MAX_DEGREE]
  --no_global_shift
  --invert              invert color range
```

Example:
```
dude@computer:~/RandomMetroidSolver (master)$ python3.7 ./customizer.py -r VARIA_Randomizer_AFX8258621_Season_Races_VARIAble.sfc --sprite megaman --patch itemsounds.ips --palette --min_degree -75 --max_degree 25 --invert
Apply patch itemsounds.ips
Apply patch megaman.ips
Customized Rom generated: Custom_VARIA_Randomizer_AFX8258621_Season_Races_VARIAble.sfc
```

# Web with Docker

You can launch the web2py website locally using docker, it has been tested on Linux, macOS and WSL2:
```
root@computer:/home/dude/RandomMetroidSolver/web/docker# ./build.sh
root@computer:/home/dude/RandomMetroidSolver/web/docker# ./run.sh
```

Then you can connect to the local website on http://127.0.0.1:8000/ on Linux/macOS and http://WSL2-local-IP:8000/ on WSL2.

You can choose the branch to checkout with -b, and give a Github token with -t to be able to do git pull in the Docker image:
```
root@computer:/home/dude/RandomMetroidSolver/web/docker# ./build.sh -b minimizer -t ~dude/RandomMetroidSolver/github_token
root@computer:/home/dude/RandomMetroidSolver/web/docker# ./run.sh -b minimizer
```

There's other scripts to start/stop the containers: start.sh / stop.sh, delete the containers/images: rm.sh and update the git repository in an image: update.sh -b branch .

# Local Development
To run your local code in a Docker container for development, you will need to pass the `-l` argument in the Docker `build` and `run` scripts to enable local mode. When using local mode, you do not need to rebuild the containers for any HTML, CSS or Javascript changes. Any changes to the Python code will require you to stop and restart. Any changes to the database will require a full rebuild of the container.

```sh
# Build the local containers
$ ./web/docker/build.sh -l

# Run the local containers
$ ./web/docker/run.sh -l

# Stop
$ ./web/docker/stop.sh

# Start
$ ./web/docker/start.sh

# Remove
$ ./web/docker/rm.sh
```

# Front end client

## For development of the tracker client

```sh
# checkout latest copy of front end client
$ git clone git@github.com:chriscauley/super-metroid

# cd into client
$ cd super-metroid/client

# install node dependencies
$ yarn install

# build client files (destination is RandomMetroidSolver/web/client)
$ yarn build:varia

# if you want to make changes to the client, run in watch mode
$ yarn watch:varia
```

## For usage of the tracker client

```sh
$ cd web
$ curl -s https://api.github.com/repos/chriscauley/super-metroid/releases/latest | jq -r '.assets[0].browser_download_url' | wget -qi - && tar zxf release.tar.gz && rm -f release.tar.gz
$ ./install.sh
```
