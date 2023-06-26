import os, json, urllib, tempfile, subprocess, base64, random
from datetime import datetime
from collections import defaultdict

from web.backend.utils import raiseHttp, loadPresetsList, updateParameterDisplay
from web.backend.utils import validateWebServiceParams, localIpsDir, getCustomMapping
from urllib.parse import urlparse, parse_qs
from utils.utils import getRandomizerDefaultParameters, removeChars, getPresetDir, PresetLoader, getPythonExec
from utils.db import DB
from logic.logic import Logic
from rom.romreader import RomReader
# custom sprites data
from varia_custom_sprites.custom_sprites import customSprites, customSpritesOrder
from varia_custom_sprites.custom_ships import customShips, customShipsOrder

from gluon.validators import IS_LENGTH, IS_MATCH, IS_NOT_EMPTY

class Customizer(object):
    def __init__(self, session, request, cache):
        self.session = session
        self.request = request
        self.cache = cache
        # required for GraphUtils access to access points
        Logic.factory('vanilla')

        self.vars = self.request.vars

    def run(self):
        self.initCustomSprites()
        self.initCustomizerSession()
        musics = self.loadMusics()
        (stdPresets, tourPresets, comPresets) = loadPresetsList(self.cache)

        url = self.request.env.request_uri.split("?")[0].split('/')
        msg = ""
        seedInfo = None
        seedParams = None
        defaultParams = None
        if len(url) > 0 and url[-1] != 'customizer':
            # a seed unique key was passed as parameter
            key = url[-1]

            # decode url
            key = urllib.parse.unquote(key)

            # sanity check
            if IS_MATCH('^[0-9a-z-]*$')(key)[1] is not None:
                msg = "Seed key can only contain [0-9a-z-]"
            elif IS_LENGTH(maxsize=36, minsize=36)(key)[1] is not None:
                msg = "Seed key must be 36 chars long"
            else:
                with DB() as db:
                    seedInfo = db.getSeedInfo(key)
                if seedInfo is None or len(seedInfo) == 0:
                    msg = "Seed {} not found".format(key)
                    seedInfo = None
                else:
                    # get a dict with seed info and another one with seed parameters
                    info = {}
                    seedParams = {}
                    infoKeys = ['time', 'filename', 'preset', 'runtime', 'complexity', 'upload_status', 'seed', 'raceMode']
                    noReplaceKeys = ['progressionDifficulty', 'progressionDifficultyMultiSelect']
                    for (k, value) in seedInfo:
                        if k in infoKeys:
                            info[k] = value
                        else:
                            if k in noReplaceKeys:
                                seedParams[k] = value
                            else:
                                seedParams[k] = updateParameterDisplay(value)
                    seedInfo = info
                    seedInfo['key'] = key

                    # if new parameters have been added since the seed creation, add them with value "n/a"
                    defaultParams = getRandomizerDefaultParameters()
                    for k in defaultParams:
                        if k not in infoKeys and k not in seedParams:
                            seedParams[k] = "n/a"

                    # check that the seed ips is available
                    if seedInfo["upload_status"] not in ['pending', 'uploaded', 'local']:
                        msg = "Seed {} not available".format(key)
                        seedInfo = None
                        seedParams = None
                    # accessing the url tell us to store the ips for more than 7 days
                    elif seedInfo["upload_status"] == 'local':
                        with DB() as db:
                            db.updateSeedUploadStatus(key, 'pending')

        query = parse_qs(urlparse(self.request.env.request_uri).query)
        if query.get('msg'):
            query_msg = query['msg'][0]
            if query_msg and msg and not query_msg.endswith('<br/>'):
                # make sure they are on separate lines if a previous msg exists
                query_msg += '<br />'
            msg = query_msg + msg

        return dict(customSprites=customSprites, customShips=customShips, musics=musics, comPresets=comPresets,
                    seedInfo=seedInfo, seedParams=seedParams, msg=msg, defaultParams=defaultParams,
                    flavorPatches=RomReader.flavorPatches)

    def initCustomizerSession(self):
        if self.session.customizer is None:
            self.session.customizer = {}

            self.session.customizer['logic'] = "vanilla"
            self.session.customizer['colorsRandomization'] = "off"
            self.session.customizer['suitsPalettes'] = "on"
            self.session.customizer['beamsPalettes'] = "on"
            self.session.customizer['tilesPalettes'] = "on"
            self.session.customizer['enemiesPalettes'] = "on"
            self.session.customizer['bossesPalettes'] = "on"
            self.session.customizer['minDegree'] = -15
            self.session.customizer['maxDegree'] = 15
            self.session.customizer['invert'] = "on"
            self.session.customizer['globalShift'] = "on"
            self.session.customizer['customSpriteEnable'] = "off"
            self.session.customizer['customSprite'] = "samus"
            self.session.customizer['customSpriteMultiSelect'] = list(customSprites.keys())
            self.session.customizer['customItemsEnable'] = "off"
            self.session.customizer['noSpinAttack'] = "off"
            self.session.customizer['customShipEnable'] = "off"
            self.session.customizer['customShip'] = "Red-M0nk3ySMShip1"
            self.session.customizer['customShipMultiSelect'] = list(customShips.keys())
            self.session.customizer['gamepadMapping'] = "off"
            self.session.customizer['preset'] = ""
            self.session.customizer['itemsounds'] = "off"
            self.session.customizer['spinjumprestart'] = "off"
            self.session.customizer['rando_speed'] = "off"
            self.session.customizer['elevators_speed'] = "off"
            self.session.customizer['fast_doors'] = "off"
            self.session.customizer['Infinite_Space_Jump'] = "off"
            self.session.customizer['refill_before_save'] = "off"
            self.session.customizer['widescreen'] = "off"
            self.session.customizer['AimAnyButton'] = "off"
            self.session.customizer['max_ammo_display'] = "off"
            self.session.customizer['supermetroid_msu1'] = "off"
            self.session.customizer['remove_itemsounds'] = "off"
            self.session.customizer['remove_spinjumprestart'] = "off"
            self.session.customizer['remove_elevators_speed'] = "off"
            self.session.customizer['remove_fast_doors'] = "off"
            self.session.customizer['remove_Infinite_Space_Jump'] = "off"
            self.session.customizer['remove_rando_speed'] = "off"
            self.session.customizer['lava_acid_physics'] = "off"
            self.session.customizer['hell'] = "off"
            self.session.customizer['hellrun_rate'] = 100
            self.session.customizer['etanks'] = 0
            self.session.customizer['hard_mode'] = "off"
            self.session.customizer['music'] = "Don't touch"
            self.session.customizer['color_blind'] = "off"
            self.session.customizer['disable_screen_shake'] = "off"
            self.session.customizer['noflashing'] = "off"

            musics = self.loadMusics()
            for song, songId in musics["_list"]:
                self.session.customizer[songId] = song

    def initCustomSprites(self):
        def updateSpriteDict(spriteDict, order):
            for i in range(len(order)):
                spriteDict[order[i]]['index'] = i
        updateSpriteDict(customSprites, customSpritesOrder)
        updateSpriteDict(customShips, customShipsOrder)

    def customWebService(self):
        print("customWebService")

        # check validity of all parameters
        switchs = ['itemsounds', 'spinjumprestart', 'rando_speed', 'elevators_speed', 'fast_doors',
                   'AimAnyButton', 'max_ammo_display', 'supermetroid_msu1', 'Infinite_Space_Jump', 'refill_before_save',
                   'customSpriteEnable', 'customItemsEnable', 'noSpinAttack', 'customShipEnable', 'remove_itemsounds',
                   'remove_elevators_speed', 'remove_fast_doors', 'remove_Infinite_Space_Jump',
                   'remove_rando_speed', 'remove_spinjumprestart', 'gamepadMapping', 'widescreen',
                   'hell', 'lava_acid_physics', 'colorsRandomization', 'suitsPalettes', 'beamsPalettes',
                   'tilesPalettes', 'enemiesPalettes', 'bossesPalettes', 'invert',
                   'color_blind', 'disable_screen_shake', 'noflashing', 'hard_mode']
        others = ['minDegree', 'maxDegree', 'hellrun_rate', 'etanks', 'logic']
        validateWebServiceParams(self.request, switchs, [], [], others, isJson=True)
        if self.vars.customSpriteEnable == 'on':
            if self.vars.customSprite == 'random':
                for sprite in self.vars.customSpriteMultiSelect.split(','):
                    if sprite not in customSprites:
                        raiseHttp(400, "Wrong value for customSpriteMultiSelect", True)
            elif self.vars.customSprite not in customSprites:
                raiseHttp(400, "Wrong value for customSprite", True)
        if self.vars.customShipEnable == 'on':
            if self.vars.customShip  == 'random':
                for ship in self.vars.customShipMultiSelect.split(','):
                    if ship not in customShips:
                        raiseHttp(400, "Wrong value for customShipMultiSelect", True)
            elif self.vars.customShip not in customShips:
                raiseHttp(400, "Wrong value for customShip", True)

        if self.vars.music not in ["Don't touch", "Disable", "Randomize", "Customize", "Restore"]:
            raiseHttp(400, "Wrong value for music", True)

        if self.vars.logic is None:
            raiseHttp(400, "Missing logic parameter", True)

        if self.session.customizer is None:
            self.session.customizer = {}

        # update session
        self.session.customizer['logic'] = self.vars.logic
        self.session.customizer['colorsRandomization'] = self.vars.colorsRandomization
        self.session.customizer['suitsPalettes'] = self.vars.suitsPalettes
        self.session.customizer['beamsPalettes'] = self.vars.beamsPalettes
        self.session.customizer['tilesPalettes'] = self.vars.tilesPalettes
        self.session.customizer['enemiesPalettes'] = self.vars.enemiesPalettes
        self.session.customizer['bossesPalettes'] = self.vars.bossesPalettes
        self.session.customizer['minDegree'] = self.vars.minDegree
        self.session.customizer['maxDegree'] = self.vars.maxDegree
        self.session.customizer['invert'] = self.vars.invert
        self.session.customizer['globalShift'] = self.vars.globalShift
        self.session.customizer['customSpriteEnable'] = self.vars.customSpriteEnable
        self.session.customizer['customSprite'] = self.vars.customSprite
        if self.vars.customSprite == 'random':
            self.session.customizer['customSpriteMultiSelect'] = self.vars.customSpriteMultiSelect.split(',')
        self.session.customizer['customItemsEnable'] = self.vars.customItemsEnable
        self.session.customizer['noSpinAttack'] = self.vars.noSpinAttack
        self.session.customizer['customShipEnable'] = self.vars.customShipEnable
        self.session.customizer['customShip'] = self.vars.customShip
        if self.vars.customShip == 'random':
            self.session.customizer['customShipMultiSelect'] = self.vars.customShipMultiSelect.split(',')
        self.session.customizer['gamepadMapping'] = self.vars.gamepadMapping
        if self.session.customizer['gamepadMapping'] == "on":
            self.session.customizer['preset'] = self.vars.preset
        self.session.customizer['itemsounds'] = self.vars.itemsounds
        self.session.customizer['spinjumprestart'] = self.vars.spinjumprestart
        self.session.customizer['rando_speed'] = self.vars.rando_speed
        self.session.customizer['elevators_speed'] = self.vars.elevators_speed
        self.session.customizer['fast_doors'] = self.vars.fast_doors
        self.session.customizer['Infinite_Space_Jump'] = self.vars.Infinite_Space_Jump
        self.session.customizer['refill_before_save'] = self.vars.refill_before_save
        self.session.customizer['widescreen'] = self.vars.widescreen
        self.session.customizer['AimAnyButton'] = self.vars.AimAnyButton
        self.session.customizer['max_ammo_display'] = self.vars.max_ammo_display
        self.session.customizer['supermetroid_msu1'] = self.vars.supermetroid_msu1
        self.session.customizer['remove_itemsounds'] = self.vars.remove_itemsounds
        self.session.customizer['remove_elevators_speed'] = self.vars.remove_elevators_speed
        self.session.customizer['remove_fast_doors'] = self.vars.remove_fast_doors
        self.session.customizer['remove_spinjumprestart'] = self.vars.remove_spinjumprestart
        self.session.customizer['remove_Infinite_Space_Jump'] = self.vars.remove_Infinite_Space_Jump
        self.session.customizer['remove_rando_speed'] = self.vars.remove_rando_speed
        self.session.customizer['lava_acid_physics'] = self.vars.lava_acid_physics
        self.session.customizer['hell'] = self.vars.hell
        self.session.customizer['hellrun_rate'] = self.vars.hellrun_rate
        self.session.customizer['etanks'] = self.vars.etanks
        self.session.customizer['hard_mode'] = self.vars.hard_mode
        self.session.customizer['music'] = self.vars.music
        self.session.customizer['color_blind'] = self.vars.color_blind
        self.session.customizer['disable_screen_shake'] = self.vars.disable_screen_shake
        self.session.customizer['noflashing'] = self.vars.noflashing

        if self.vars.music == 'Customize':
            musics = self.loadMusics()
            for song, songId in musics["_list"]:
                self.session.customizer[songId] = self.vars[songId]

        # when beam doors patch is detected, don't randomize blue door palette
        no_blue_door_palette = self.vars.no_blue_door_palette

        # call the randomizer
        (fd, jsonFileName) = tempfile.mkstemp()
        params = [getPythonExec(),  os.path.expanduser("~/RandomMetroidSolver/customizer.py"),
                  '--output', jsonFileName, '--logic' , self.vars.logic]

        if self.vars.itemsounds == 'on':
            params += ['-c', 'itemsounds.ips']
        if self.vars.elevators_speed == 'on':
            params += ['-c', 'elevators_speed.ips']
        if self.vars.fast_doors == 'on':
            params += ['-c', 'fast_doors.ips']
        if self.vars.spinjumprestart == 'on':
            params += ['-c', 'spinjumprestart.ips']
        if self.vars.rando_speed == 'on':
            params += ['-c', 'rando_speed.ips']
        if self.vars.AimAnyButton == 'on':
            params += ['-c', 'AimAnyButton.ips']
        if self.vars.max_ammo_display == 'on':
            params += ['-c', 'max_ammo_display.ips']
        if self.vars.supermetroid_msu1 == 'on':
            params += ['-c', 'supermetroid_msu1.ips']
        if self.vars.Infinite_Space_Jump == 'on':
            params += ['-c', 'Infinite_Space_Jump']
        if self.vars.refill_before_save == 'on':
            params += ['-c', 'refill_before_save.ips']
        if self.vars.widescreen == 'on':
            params += ['-c', 'widescreen.ips']
        if self.vars.remove_itemsounds == 'on':
            params += ['-c', 'remove_itemsounds.ips']
        if self.vars.remove_elevators_speed == 'on':
            params += ['-c', 'remove_elevators_speed.ips']
        if self.vars.remove_fast_doors == 'on':
            params += ['-c', 'remove_fast_doors.ips']
        if self.vars.remove_rando_speed == 'on':
            params += ['-c', 'remove_rando_speed.ips']
        if self.vars.remove_spinjumprestart == 'on':
            params += ['-c', 'remove_spinjumprestart.ips']
        if self.vars.remove_Infinite_Space_Jump == 'on':
            params += ['-c', 'remove_Infinite_Space_Jump.ips']
        if self.vars.music == 'Disable':
            params += ['-c', 'No_Music']
        if self.vars.music == 'Randomize':
            params += ['-c', 'random_music.ips']
        if self.vars.music == 'Restore':
            params += ['-c', 'vanilla_music.ips']
        if self.vars.lava_acid_physics == 'on':
            params += ['-c', 'lava_acid_physics.ips']
        if self.vars.hell == 'on':
            params += ['-c', 'hell.ips']
        if self.vars.hellrun_rate != 'off':
            params += ['--hellrun', self.vars.hellrun_rate]
        if self.vars.etanks != 'off':
            params += ['--etanks', self.vars.etanks]
        if self.vars.hard_mode != 'off':
            params += ['-c', 'hard_mode.ips']
        if self.vars.color_blind == 'on':
            params += ['-c', 'color_blind.ips']
        if self.vars.disable_screen_shake == 'on':
            params += ['-c', 'disable_screen_shake.ips']
        if self.vars.noflashing == 'on':
            params += ['-c', 'noflashing.ips']

        if self.vars.colorsRandomization == 'on':
            params.append('--palette')
            if self.vars.suitsPalettes == 'off':
                params.append('--no_shift_suit_palettes')
            if self.vars.beamsPalettes == 'off':
                params.append('--no_shift_beam_palettes')
            if self.vars.tilesPalettes == 'off':
                params.append('--no_shift_tileset_palette')
            if self.vars.enemiesPalettes == 'off':
                params.append('--no_shift_enemy_palettes')
            if self.vars.bossesPalettes == 'off':
                params.append('--no_shift_boss_palettes')
            if self.vars.globalShift == 'off':
                params.append('--no_global_shift')
                params.append('--individual_suit_shift')
                params.append('--individual_tileset_shift')
                params.append('--no_match_ship_and_power')
            params += ['--min_degree', self.vars.minDegree, '--max_degree', self.vars.maxDegree]
            if self.vars.invert == 'on':
                params.append('--invert')
            if no_blue_door_palette == 'on':
                params.append('--no_blue_door_palette')

        if self.vars.customSpriteEnable == 'on':
            if self.vars.customSprite == 'random':
                sprite = random.choice(self.session.customizer['customSpriteMultiSelect'])
            else:
                sprite = self.vars.customSprite

            params += ['--sprite', sprite]
            with DB() as db:
                db.addSprite(sprite)
            if self.vars.customItemsEnable == 'on':
                params.append('--customItemNames')
            if self.vars.noSpinAttack == 'on':
                params.append('--no_spin_attack')
        if self.vars.customShipEnable == 'on':
            if self.vars.customShip == 'random':
                ship = random.choice(self.session.customizer['customShipMultiSelect'])
            else:
                ship = self.vars.customShip

            params += ['--ship', "{}.ips".format(ship)]
            with DB() as db:
                db.addShip(ship)
            if customShips[ship].get("hideSamus", False):
                params += ['-c', 'custom_ship.ips']
            if customShips[ship].get("showSamusAtTakeoff", False):
                params += ['-c', 'Ship_Takeoff_Disable_Hide_Samus']
        if self.vars.seedKey != None:
            with DB() as db:
                seedIpsInfo = db.getSeedIpsInfo(self.vars.seedKey)
            print("seedIpsInfo: {}".format(seedIpsInfo))
            if seedIpsInfo == None or len(seedIpsInfo) == 0:
                raiseHttp(400, json.dumps("Can't get seed info"))
            (uploadStatus, fileName) = seedIpsInfo[0]
            if uploadStatus not in ['local', 'pending', 'uploaded']:
                raiseHttp(400, json.dumps("Seed is not available"))

            ipsFileName = os.path.join(localIpsDir, self.vars.seedKey, fileName.replace('sfc', 'ips'))
            params += ['--seedIps', ipsFileName]

        if self.vars.music == "Customize":
            musics = self.loadMusics()
            customMusic = {
                'params': {
                    "varia": self.vars.varia == "true",
                    "area": self.vars.area == "true",
                    "boss": self.vars.boss == "true"
                }, 'mapping': {}}
            for song, songId in musics["_list"]:
                newSong = self.vars[songId]
                if newSong not in musics:
                    raiseHttp(400, "unknown song for {}".format(song))
                if newSong != song:
                    customMusic['mapping'][song] = newSong
            (fd2, jsonMusicFileName) = tempfile.mkstemp()
            with open(jsonMusicFileName, 'w') as musicFile:
                json.dump(customMusic, musicFile)
            params += ['--music', jsonMusicFileName]

        if self.vars.gamepadMapping == "on":
            preset = self.vars.preset
            fullPath = '{}/{}.json'.format(getPresetDir(preset), preset)
            controlMapping = PresetLoader.factory(fullPath).params['Controller']
            (custom, controlParam) = getCustomMapping(controlMapping)
            if custom == True:
                print("apply custom gamepad mapping from preset: {}".format(self.vars.preset))
                params += ['--controls', controlParam]
                if "Moonwalk" in controlMapping and controlMapping["Moonwalk"] == True:
                    params.append('--moonwalk')

        print("before calling: {}".format(params))
        start = datetime.now()
        ret = subprocess.call(params)
        end = datetime.now()
        duration = (end - start).total_seconds()
        print("ret: {}, duration: {}s".format(ret, duration))

        if self.vars.music == "Customize":
            os.close(fd2)
            os.remove(jsonMusicFileName)

        if ret == 0:
            with open(jsonFileName) as jsonFile:
                data = json.load(jsonFile)

            os.close(fd)
            os.remove(jsonFileName)

            return json.dumps(data)
        else:
            # extract error from json
            try:
                with open(jsonFileName) as jsonFile:
                    msg = json.load(jsonFile)['errorMsg']
            except:
                msg = "customizerWebService: something wrong happened"

            os.close(fd)
            os.remove(jsonFileName)
            raiseHttp(400, json.dumps(msg))

    def loadMusics(self):
        musics = self.cache.ram('musics', lambda:dict(), time_expire=None)
        if musics:
            return musics

        hiddenGroups = ["Vanilla Soundtrack - Sound Effects", "Memory Violation"]

        musicDir = 'music/_metadata'
        dropdown = defaultdict(list)
        metadatas = sorted(os.listdir(musicDir), key=lambda v: v.upper())
        for metadata in metadatas:
            with open(os.path.join(musicDir, metadata), 'r', encoding='utf-8') as jsonFile:
                data = json.load(jsonFile)
                defaultGroup = os.path.splitext(metadata)[0]
                musics.update(data)
                # check if there's group for musics
                for song, songData in data.items():
                    group = songData.get("group", defaultGroup)
                    if group in hiddenGroups:
                        continue
                    dropdown[group].append(song)
        musics["_dropdown"] = dropdown

        with open('music/_metadata/vanilla.json', 'r', encoding='utf-8') as jsonFile:
            vanilla = json.load(jsonFile)
        with open('music/_constraints/vanilla.json', 'r', encoding='utf-8') as jsonFile:
            constraints = json.load(jsonFile)
        musics["_list"] = [(song, removeChars(song, " ,()-/")) for song in vanilla.keys() if song not in constraints["preserve"] and song not in constraints["discard"]]
        return musics

    def getSpcFile(self):
        songName = self.vars.songName
        if IS_NOT_EMPTY()(songName)[1] is not None:
            raiseHttp(400, "Song is empty")
        if IS_MATCH('[a-zA-Z0-9_\.() ,\-/]*', strict=True)(songName)[1] is not None:
            raiseHttp(400, "Invalid char in song name")
        if IS_LENGTH(64)(songName)[1] is not None:
            raiseHttp(400, "Song must be max 64 chars")
        print("getSpcFile songName: {}".format(songName))

        musics = self.loadMusics()
        if songName not in musics:
            raiseHttp(400, "No preview for this song")

        if 'spc_path' not in musics[songName] or musics[songName]['spc_path'] == "":
            raiseHttp(400, "No preview for this song")

        songFile = musics[songName]['spc_path']
        with open(os.path.join('music', songFile), 'rb') as spcFile:
            spcFileData = spcFile.read()
            return json.dumps({'spc': base64.b64encode(spcFileData).decode()})
