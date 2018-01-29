# -*- coding: utf-8 -*-

import sys, os.path
path = os.path.expanduser('~/RandomMetroidSolver')
if os.path.exists(path) and path not in sys.path:
    sys.path.append(path)

import datetime, os, hashlib

# to solve the rom
from parameters import *
from helpers import *
import tournament_locations
from solver import *

difficulties = {
    0: 'mania',
    easy : 'easy',
    medium : 'medium',
    hard : 'hard',
    harder : 'very hard',
    hardcore : 'hardcore',
    mania : 'mania'
}

difficulties2 = {
    'easy' : easy,
    'medium' : medium,
    'hard' : hard,
    'harder' : harder,
    'very hard': harder,
    'hardcore' : hardcore,
    'mania' : mania
}

desc = {'Mockball': {'display': 'Mockball',
                     'title': 'Early Super and Ice Beam',
                     'href': 'https://wiki.supermetroid.run/index.php?title=Mockball'},
        'SimpleShortCharge': {'display': 'Simple Short Charge',
                              'title': 'Waterway ETank without gravity, and Wrecked Ship access',
                              'href': 'https://wiki.supermetroid.run/index.php?title=Quick_charge'},
        'InfiniteBombJump': {'display': 'Infinite Bomb Jump',
                             'title': 'To access certain locations without high jump or space jump',
                             'href': 'https://www.youtube.com/watch?v=Qfmcm7hkXP4'},
        'GreenGateGlitch': {'display': 'Green Gate Glitch',
                            'title': 'To access screw attack and crocomire',
                            'href': 'https://wiki.supermetroid.run/index.php?title=Gate_Glitch'},
        'ShortCharge': {'display': 'Short Charge',
                        'title': 'To kill draygon',
                        'href': 'https://wiki.supermetroid.run/index.php?title=Short_Charge'},
        'GravityJump': {'display': 'Gravity Jump',
                        'title': 'Super high jumps in water/lava',
                        'href': 'https://wiki.supermetroid.run/index.php?title=14%25#Gravity_Jump'},
        'SpringBallJump': {'display': 'Spring Ball Jump',
                           'title': 'Access to wrecked ship etank without anything else, suitless maridia navigation',
                           'href': 'https://www.youtube.com/watch?v=8ldQUIgBavw&t=49s'},
        'SpringBallJumpFromWall': {'display': 'Spring Ball Jump from wall',
                                   'title': 'Exit Screw Attack area, climb Worst Room without High Jump',
                                   'href': None},
        'GetAroundWallJump': {'display': 'Get around Wall Jump',
                              'title': 'Tricky wall jumps where you have to get around the platform you want to wall jump on (access Norfair Reserve, go through Worst Room in the game, exit Plasma Room)',
                              'href': 'https://www.youtube.com/watch?v=2GPx-6ARSIw&t=137s'},
        'DraygonGrappleKill': {'display': 'Draygon Grapple Kill',
                               'title': 'Instant kill on Draygon with electric grapple',
                               'href': 'https://www.youtube.com/watch?v=gcemRrXqCbE'},
        'MicrowaveDraygon': {'display': 'Microwave Draygon',
                             'title': 'Charge/Plasma/X-Ray glitch on Draygon',
                             'href': 'https://www.youtube.com/watch?v=tj0VybUH6ZY'},
        'MicrowavePhantoon': {'display': 'Microwave Phantoon',
                              'title': 'Same as Draygon, with a few missiles to start',
                              'href': None},
        'IceZebSkip': {'display': 'Ice Zeb Skip',
                       'title': 'Skip the Zebetites with Ice beam',
                       'href': 'https://www.youtube.com/watch?v=GBXi3MSpGZg'},
        'SpeedZebSkip': {'display': 'Speed Zeb Skip',
                         'title': 'Skip the Zebetites with a shinespark',
                         'href': 'https://www.youtube.com/watch?v=jEAgdWQ9kLQ'},
        'CeilingDBoost': {'display': 'Ceiling Damage Boost',
                          'title': 'Hit an enemy at the right time to get the item in Blue Brinstar Ceiling',
                          'href': 'https://www.metroid2002.com/3/early_items_blue_brinstar_energy_tank.php'},
        'AlcatrazEscape': {'display': 'Alcatraz Escape',
                           'title': 'Escape from Bomb area using its entrance tunnel',
                           'href': 'https://www.youtube.com/watch?v=XSBeLJJafjY'},
        'ReverseGateGlitch': {'display': 'Reverse Gate Glitch',
                              'title': 'Open wave gate in Pink Brinstar from bottom left corner with High Jump',
                              'href': 'https://www.youtube.com/watch?v=cykJDBBSBrc'},
        'ReverseGateGlitchHiJumpLess': {'display': 'Reverse Gate Glitch without High Jump',
                              'title': 'Open wave gate in Pink Brinstar from bottom left corner without High Jump',
                              'href': None},
        'EarlyKraid': {'display': 'Early Kraid',
                       'title': 'Access Kraid area by wall jumping',
                       'href': 'https://www.youtube.com/watch?v=rHMHqTHHqHs'},
        'XrayDboost': {'display': 'X-Ray Damage Boost',
                       'title': 'Get to X-Ray location without Space Jump or Grapple',
                       'href': 'https://www.youtube.com/watch?v=2GPx-6ARSIw&t=162s'},
        'XrayIce': {'display': 'X-Ray Ice',
                    'title': 'Get to X-Ray location by freezing enemies',
                    'href': None},
        'RedTowerClimb': {'display': 'Red Tower Climb',
                          'title': 'Climb Red Tower without Ice or Screw Attack',
                          'href': 'https://www.youtube.com/watch?v=g3goe6PZ4o0'},
        'HiJumpLessGauntletAccess': {'display': 'Gauntlet Access without High Jump',
                                 'title': 'Access Gauntlet area using really tricky wall jumps',
                                 'href': 'https://www.youtube.com/watch?v=uVU2X-egOTI&t=25s'},
        'HiJumpGauntletAccess': {'display': 'Hi-Jump Gauntlet Access',
                                 'title': 'Access Gauntlet area using tricky wall jumps',
                                 'href': 'https://www.youtube.com/watch?v=2a6mf-kB60U'},
        'GauntletWithBombs': {'display': 'Gauntlet With Bombs',
                              'title': 'Traverse Gauntlet area with only bombs',
                              'href': 'https://www.youtube.com/watch?v=HZ8589lLlAg'},
        'GauntletWithPowerBombs': {'display':
                                   'Gauntlet With Power-Bombs',
                                   'title': 'Traverse Gauntlet area with power bombs',
                                   'href': None},
        'GauntletEntrySpark': {'display': 'Gauntlet Entry Spark',
                               'title': 'Traverse Gauntlet area with a Shine spark',
                               'href': 'https://www.youtube.com/watch?v=rFobt0S5sD4'},
        'NorfairReserveIce': {'display': 'Norfair Reserve Ice',
                              'title': 'Climb to Norfair Reserve area by freezing a Waver',
                              'href': None},
        'WaveBeamWallJump': {'display': 'Wave-Beam Wall-Jump',
                             'title': 'Climb to Wave Beam with wall jumps',
                             'href': 'https://www.youtube.com/watch?v=2GPx-6ARSIw&t=140s'},
        'ClimbToGrappleWithIce': {'display': 'Climb to Grapple With Ice',
                                  'title': 'Climb to Grapple Beam area using Ice Beam and bugs in Post Crocomire Jump Room',
                                  'href': None},
        'LavaDive': {'display': 'Lava Dive',
                     'title': 'Enter Lower Norfair with Varia ans Hi Jump',
                     'href': 'https://www.youtube.com/watch?v=pdyBy_54dB0'},
        'WorstRoomIceCharge': {'display': 'Worst Room Ice and Charge',
                               'title': 'Go through Worst Room In The Game JUST by freezing pirates',
                               'href': 'https://www.youtube.com/watch?v=AYK7LREbLI8'},
        'ScrewAttackExit': {'display': 'Screw Attack Exit',
                            'title': 'Gain momentum from Golden Torizo Energy Recharge room, then wall jump in Screw Attack room',
                            'href': None},
        'ContinuousWallJump': {'display': 'Continuous Wall-Jump',
                               'title': 'Get over the moat using CWJ',
                               'href': 'https://www.youtube.com/watch?v=4HVhTwwax6g'},
        'DiagonalBombJump': {'display': 'Diagonal Bomb-Jump',
                             'title': 'Get over the moat using bomb jumps',
                             'href': 'https://www.youtube.com/watch?v=9Q8WGKCVb40'},
        'MockballWs': {'display': 'Mockball Wrecked Ship',
                       'title': 'Get over the moat using mockball and Spring Ball',
                       'href': 'https://www.youtube.com/watch?v=WYxtRF--834'},
        'SpongeBathBombJump': {'display': 'SpongeBath Bomb-Jump',
                               'title': 'Get through sponge bath room (before spiky room of death) with bomb jumps',
                               'href': 'https://www.youtube.com/watch?v=8ldQUIgBavw'},
        'SpongeBathHiJump': {'display': 'SpongeBath Hi-Jump',
                             'title': 'Get through sponge bath room (before spiky room of death) with Hi Jump and walljumps',
                             'href': 'https://www.youtube.com/watch?v=8ldQUIgBavw'},
        'SpongeBathSpeed': {'display': 'SpongeBath Speed',
                            'title': 'Get through sponge bath room (before spiky room of death) with Speed Boster and walljumps',
                            'href': 'https://www.youtube.com/watch?v=8ldQUIgBavw'},
        'SuitlessOuterMaridia': {'display': 'Suitless Outer Maridia',
                                 'title': 'Make your way through Maridia (up to Botwoon area) with Hi Jump, Grapple and Ice',
                                 'href': 'https://www.youtube.com/watch?v=c2xoPigezvM'},
        'SuitlessOuterMaridiaNoGuns': {'display': 'Suitless Outer Maridia with no Guns',
                                       'title': 'Same as above, but with no firepower besides Ice Beam',
                                       'href': 'https://www.youtube.com/watch?v=c2xoPigezvM'},
        'MamaGrappleWithWallJump': {'display': 'Mama Grapple with Wall Jump',
                                    'title': 'Get to Grapple block with with just Grapple and Wall Jumps',
                                    'href': None},
        'DraygonRoomGrappleExit': {'display': 'Exit Draygon room with the Grapple',
                                 'title': 'Use Grapple to bounce them morph and demorph up to the platform',
                                 'href': 'https://www.youtube.com/watch?v=i2OGuFpcfiw&t=154s'},
        'DraygonRoomCrystalExit': {'display': 'Exit Draygon room with a shine spark',
                                 'title': 'Doing a Crystal flash and being grabbed by Draygon gives a free shine spark',
                                 'href': 'https://www.youtube.com/watch?v=hrHHfvGD3wo&t=625s'},
        'PreciousRoomXRayExit': {'display': 'Exit the Precious room with an Xray glitch',
                                 'title': 'Use an XrayScope glitch to climb out of the Precious room',
                                 'href': 'https://www.youtube.com/watch?v=i2OGuFpcfiw&t=160s'},
        'MochtroidClip': {'display': 'Mochtroid Clip',
                          'title': 'Get to Botwoon with Ice Beam',
                          'href': 'https://wiki.supermetroid.run/index.php?title=14%25#Mochtroid_Clip'},
        'PuyoClip': {'display': 'Puyo Clip',
                     'title': 'Get to Spring Ball with Gravity Suit and Ice Beam',
                     'href': 'https://www.youtube.com/watch?v=e5ZH_9paSLw'},
        'KillPlasmaPiratesWithSpark': {'display': 'Kill Plasma Pirates with Spark',
                                       'title': 'Use shinesparks to kill the pirates in Plasma Beam room',
                                       'href': None},
        'KillPlasmaPiratesWithCharge': {'display': 'Kill Plasma Pirates with Charge',
                                        'title': 'Use pseudo-screw to kill the pirates in Plasma Beam room',
                                        'href': None},
        'SuitlessSandpit': {'display': 'Suitless Sandpit',
                            'title': 'Access item in the left sandpit without Gravity',
                            'href': 'https://www.youtube.com/watch?v=1M2TiEVwH2I'}
}

usedAcrossTheGame = ['Mockball', 'SimpleShortCharge', 'InfiniteBombJump', 'GreenGateGlitch', 'ShortCharge', 'GravityJump', 'SpringBallJump', 'SpringBallJumpFromWall', 'GetAroundWallJump']
bosses = ['DraygonGrappleKill', 'MicrowaveDraygon', 'MicrowavePhantoon']
endGame = ['IceZebSkip', 'SpeedZebSkip']
brinstar = ['CeilingDBoost', 'AlcatrazEscape', 'ReverseGateGlitch', 'ReverseGateGlitchHiJumpLess', 'EarlyKraid', 'XrayDboost', 'XrayIce', 'RedTowerClimb']
gauntlet = ['HiJumpLessGauntletAccess', 'HiJumpGauntletAccess', 'GauntletWithBombs', 'GauntletWithPowerBombs', 'GauntletEntrySpark']
upperNorfair = ['NorfairReserveIce', 'WaveBeamWallJump', 'ClimbToGrappleWithIce']
lowerNorfair = ['LavaDive', 'ScrewAttackExit', 'WorstRoomIceCharge']
wreckedShip = ['ContinuousWallJump', 'DiagonalBombJump', 'MockballWs']
wreckedShipEtank = ['SpongeBathBombJump', 'SpongeBathHiJump', 'SpongeBathSpeed']
maridiaSuitless = ['SuitlessOuterMaridia', 'SuitlessOuterMaridiaNoGuns']
maridiaMama = ['MamaGrappleWithWallJump']
maridiaSuitlessDraygon = ['DraygonRoomGrappleExit', 'DraygonRoomCrystalExit', 'PreciousRoomXRayExit']
maridiaClips = ['MochtroidClip', 'PuyoClip']
maridiaPlasmaRoom = ['KillPlasmaPiratesWithSpark', 'KillPlasmaPiratesWithCharge']
maridiaSandpit = ['SuitlessSandpit']

categories = [{'knows': usedAcrossTheGame, 'title': 'Used across the game'},
              {'knows': bosses, 'title': 'Bosses'},
              {'knows': endGame, 'title': 'End Game'},
              {'knows': brinstar, 'title': 'Brinstar'},
              {'knows': gauntlet, 'title': 'Gauntlet'},
              {'knows': upperNorfair, 'title': 'Upper Norfair'},
              {'knows': lowerNorfair, 'title': 'Lower Norfair'},
              {'knows': wreckedShip, 'title': 'Wrecked Ship'},
              {'knows': wreckedShipEtank, 'title': 'Wrecked Ship Etank'},
              {'knows': maridiaSuitless, 'title': 'Maridia Suitless'},
              {'knows': maridiaMama, 'title': 'Mama Turtle'},
              {'knows': maridiaSuitlessDraygon, 'title': 'Maridia Suitless Draygon'},
              {'knows': maridiaClips, 'title': 'Maridia Clips'},
              {'knows': maridiaPlasmaRoom, 'title': 'Maridia Plasma Room'},
              {'knows': maridiaSandpit, 'title': 'Maridia Sandpit'}]

def solver():
    # load conf from session if available
    loaded = False
    if session.paramsFile is None:
        # default preset
        session.paramsFile = 'regular'

    if request.post_vars._formname is not None:
        # press solve, load or save button
        if request.post_vars._formname in ['saveform', 'mainform']:
            # store the changes in case the form won't be accepted
            paramsDict = generate_json_from_parameters(request.post_vars,
                                                       hidden=(request.post_vars._formname == 'saveform'))
            session.paramsDict = paramsDict
            params = ParamsLoader.factory(session.paramsDict).params
            loaded = True
        elif request.post_vars._formname in ['loadform']:
            # nothing to load, we'll load the new params file with the load form code
            pass
    else:
        # no forms button pressed
        if session.paramsDict is not None:
            params = ParamsLoader.factory(session.paramsDict).params
            loaded = True

    if not loaded:
        params = ParamsLoader.factory('diff_presets/{}.json'.format(session.paramsFile)).params

    # filter the displayed roms to display only the ones uploaded in this session
    if session.romFiles is None:
        session.romFiles = []
        roms = []
    elif len(session.romFiles) == 0:
        roms = []
    else:
        files = sorted(os.listdir('roms'))
        bases = [os.path.splitext(file)[0] for file in files]
        filtered = [base for base in bases if base in session.romFiles]
        roms = [file+'.sfc' for file in filtered]

    # main form
    mainForm = FORM(TABLE(TR("Already uploaded rom in this session:",
                             SELECT(*roms, **dict(_name="romFile", value=session.romFile+'.sfc' if session.romFile is not None else None)))),
                    TABLE(TR("Pick a randomized Super Metroid ROM to upload and solve:",
                             INPUT(_type="file",
                                   _name="uploadFile", _id="uploadFile"))),
                    TABLE(TR(INPUT(_type="submit",_value="Compute difficulty"))),
                    INPUT(_type="text", _name="json", _id="json", _style='display:none'),
                    _id="mainform", _name="mainform", _onsubmit="doSubmit();")

    if mainForm.process(formname='mainform').accepted:

        # new uploaded rom ?
        error = False
        if mainForm.vars['json'] != '':
            try:
                tempRomJson = json.loads(mainForm.vars['json'])
                romFileName = tempRomJson["romFileName"]
                (base, ext) = os.path.splitext(romFileName)
                jsonRomFileName = 'roms/' + base + '.json'
                del tempRomJson["romFileName"]

                # json keys are strings
                romJson = {}
                for address in tempRomJson:
                    romJson[int(address)] = tempRomJson[address]

                romLoader = RomLoader.factory(romJson)
                romLoader.assignItems(tournament_locations.locations)
                romLoader.dump(jsonRomFileName)

                session.romFile = base
                if base not in session.romFiles:
                    session.romFiles.append(base)
            except:
                response.flash = "Error loading the rom file"
                error = True

        # python3:
        # no file: type(mainForm.vars['uploadFile'])=[<class 'str'>]
        # file:    type(mainForm.vars['uploadFile'])=[<class 'cgi.FieldStorage'>]
        # python2:
        # no file: type(mainForm.vars['uploadFile'])=[<type 'str'>]
        # file:    type(mainForm.vars['uploadFile'])=[<type 'instance'>]
        elif mainForm.vars['uploadFile'] is not None and type(mainForm.vars['uploadFile']) != str:
            uploadFileName = mainForm.vars['uploadFile'].filename
            uploadFileContent = mainForm.vars['uploadFile'].file

            (base, ext) = os.path.splitext(uploadFileName)
            jsonRomFileName = 'roms/' + base + '.json'

            if ext not in ['.sfc', '.smc']:
                response.flash = "Rom file must be .sfc or .smc"
                error = True
            else:
                # try loading it and create a json from it
                try:
                    tempRomFile = 'roms/' + base + '.sfc'
                    with open(tempRomFile, 'wb') as tempRom:
                        tempRom.write(uploadFileContent.read())

                    romLoader = RomLoader.factory(tempRomFile)
                    romLoader.assignItems(tournament_locations.locations)
                    romLoader.dump(jsonRomFileName)

                    os.remove(tempRomFile)

                    session.romFile = base
                    if base not in session.romFiles:
                        session.romFiles.append(base)
                except:
                    response.flash = "Error loading the rom file"
                    error = True

        elif len(mainForm.vars['romFile']) != 0:
            session.romFile = os.path.splitext(mainForm.vars['romFile'])[0]
            jsonRomFileName = 'roms/' + session.romFile + '.json'

        else:
            response.flash = "No rom file selected for upload"
            error = True

        if not error:
            # check that the json file exists
            if not os.path.isfile(jsonRomFileName):
                response.flash = "Missing json rom file on the server"
            else:
                session.result = compute_difficulty(jsonRomFileName, request.post_vars)
                redirect(URL(r=request, f='solver'))

    # load form
    files = sorted(os.listdir('diff_presets'))
    presets = [os.path.splitext(file)[0] for file in files]

    loadTable = TABLE(TR("Choose an available preset:",
                         SELECT(*presets, **dict(_name="paramsFile", value=session.paramsFile, _onchange="this.form.submit()"))))
    loadForm = FORM(loadTable, _id="loadform", _name="loadform")

    if loadForm.process(formname='loadform').accepted:

        # check that the presets file exists
        paramsFile = loadForm.vars['paramsFile']
        fullPath = 'diff_presets/{}.json'.format(paramsFile)
        if os.path.isfile(fullPath):
            # load it
            params = ParamsLoader.factory(fullPath).params
            session.paramsFile = paramsFile
            # params changed, no longer display the old result to avoid confusion
            session.result = None
            session.paramsDict = None
            redirect(URL(r=request, f='solver'))
        else:
            response.flash = "Presets file not found"

    # save form
    saveTable = TABLE(TR("Update an existing preset:",
                         SELECT(*presets, **dict(_name="paramsFile", value=session.paramsFile))),
                      TR("Create a new preset:",
                         INPUT(_type="text",
                               _name="saveFile",
                               requires=[IS_ALPHANUMERIC(error_message='Preset name must be alphanumeric and max 32 chars'),
                                         IS_LENGTH(32)])),
                      TR("Password:",
                         INPUT(_type="text",
                               _name="password",
                               requires=[IS_NOT_EMPTY(),
                                         IS_ALPHANUMERIC(error_message='Password must be alphanumeric and max 32 chars'), 
                                         IS_LENGTH(32)])))
    saveTable.append(TR(INPUT(_type="submit",_value="Save presets")))
    saveForm = FORM(saveTable, _id="saveform", _name="saveform")

    if saveForm.process(formname='saveform').accepted:

        # update or creation ?
        saveFile = saveForm.vars['saveFile']
        if saveFile == "":
            saveFile = saveForm.vars['paramsFile']

        # check if the presets file already exists
        password = saveForm.vars['password']
        password = password.encode('utf-8')
        passwordSHA256 = hashlib.sha256(password).hexdigest()
        fullPath = 'diff_presets/{}.json'.format(saveFile)
        if os.path.isfile(fullPath):
            # load it
            oldParams = ParamsLoader.factory(fullPath).params

            # check if password match
            if 'password' in oldParams and passwordSHA256 == oldParams['password']:
                # update the presets file
                paramsDict = generate_json_from_parameters(request.post_vars, hidden=True)
                paramsDict['password'] = passwordSHA256
                ParamsLoader.factory(paramsDict).dump(fullPath)
                session.paramsFile = saveFile
                redirect(URL(r=request, f='solver'))
            else:
                response.flash = "Password mismatch with existing presets file {}".format(saveFile)

        else:
            # write the presets file
            paramsDict = generate_json_from_parameters(request.post_vars, hidden=True)
            paramsDict['password'] = passwordSHA256
            ParamsLoader.factory(paramsDict).dump(fullPath)
            session.paramsFile = saveFile
            redirect(URL(r=request, f='solver'))

    # conf parameters
    conf = {}
    if 'difficultyTarget' in params['Conf']:
        conf["target"] = params['Conf']['difficultyTarget']
    else:
        conf["target"] = Conf.difficultyTarget
    if 'majorsPickup' in params['Conf']:
        conf["pickup"] = params['Conf']['majorsPickup']
    else:
        conf["pickup"] = Conf.majorsPickup

    # display result
    if session.result is not None:
        if session.result['difficulty'] == -1:
            resultText = "The rom \"{}\" is not finishable with the known technics".format(session.result['randomizedRom'])
        else:
            resultText = "The rom \"{}\" estimated difficulty is: ".format(session.result['randomizedRom'])

        difficulty = session.result['difficulty']
        diffPercent = session.result['diffPercent']

        # add generated path (spoiler !)
        pathTable = TABLE(TR(TH("Location Name"), TH("Area"), TH("Item"), TH("Difficulty"), TH("Techniques used")))
        for location, area, item, diff, techniques in session.result['generatedPath']:
            pathTable.append(TR(location, area, item, diff, techniques))

        knowsUsed = session.result['knowsUsed']

        # display the result only once
        session.result = None
    else:
        resultText = None
        difficulty = None
        diffPercent = None
        pathTable = None
        knowsUsed = None

    # set title
    response.title = 'Super Metroid Item Randomizer Solver'
    response.menu = [['Super Metroid Item Randomizer Solver', False, '#'],
                     ['Solve!', True, URL(f='solver')],
                     ['Information & Contact', False, URL(f='infos')]]

    # add missing knows
    for know in Knows.__dict__:
        if know[0:len('__')] != '__':
            if know not in params['Knows'].keys():
                params['Knows'][know] = Knows.__dict__[know]

    # send values to view
    return dict(mainForm=mainForm, loadForm=loadForm, saveForm=saveForm,
                desc=desc,
                difficulties=difficulties,
                categories=categories,
                knows=params['Knows'], conf=conf, knowsUsed=knowsUsed,
                resultText=resultText, pathTable=pathTable,
                difficulty=difficulty, diffPercent=diffPercent,
                easy=easy,medium=medium,hard=hard,harder=harder,hardcore=hardcore,mania=mania)

def generate_json_from_parameters(vars, hidden):
    if hidden is True:
        hidden = "_hidden"
    else:
        hidden = ""
    paramsDict = {'Conf': {}, 'Settings': {}, 'Knows': {}}
    for var in Knows.__dict__:
        # print("var={}".format(var))
        if var[0:len('__')] != '__':
            boolVar = vars[var+"_bool"+hidden]
            # print("{} = {}".format(var+"_bool"+hidden, boolVar))
            if boolVar is None:
                paramsDict['Knows'][var] = [False, 0]
            else:
                paramsDict['Knows'][var] = [True, difficulties2[vars[var+"_diff"+hidden]]]
            # print("{}: {}".format(var, paramsDict['Knows'][var]))

    diffTarget = vars["difficulty_target"+hidden]
    #print("diffTarget={}".format(diffTarget))
    if diffTarget is not None:
        paramsDict['Conf']['difficultyTarget'] = difficulties2[diffTarget]
        #print("paramsDict['Conf']['difficultyTarget']={}".format(paramsDict['Conf']['difficultyTarget']))

    pickupStrategy = vars["pickup_strategy"+hidden]
    if pickupStrategy is not None:
        if pickupStrategy == 'all':
            paramsDict['Conf']['majorsPickup'] = 'all'
            paramsDict['Conf']['minorsPickup'] = 'all'
        elif pickupStrategy == 'any':
            paramsDict['Conf']['majorsPickup'] = 'any'
            paramsDict['Conf']['minorsPickup'] = 'any'
        else:
            paramsDict['Conf']['majorsPickup'] = 'minimal'
            paramsDict['Conf']['minorsPickup'] = {'Missile' : 10, 'Super' : 5, 'PowerBomb' : 2}

    return paramsDict

def compute_difficulty(jsonRomFileName, post_vars):
    randomizedRom = os.path.basename(jsonRomFileName.replace('json', 'sfc'))

    # generate json from parameters
    paramsDict = generate_json_from_parameters(post_vars, hidden=False)
    session.paramsDict = paramsDict

    # call solver
    solver = Solver(type='web', rom=jsonRomFileName, params=[paramsDict])
    difficulty = solver.solveRom()
    diffPercent = DifficultyDisplayer(difficulty).percent()

    generatedPath = solver.getPath(solver.visitedLocations)

    # the different knows used during the rom
    knowsUsed = solver.getKnowsUsed()
    used = len(knowsUsed)

    # the number of knows set to True
    total = len([param for param in paramsDict['Knows'] if paramsDict['Knows'][param][0] is True])

    return dict(randomizedRom=randomizedRom, difficulty=difficulty,
                generatedPath=generatedPath, diffPercent=diffPercent,
                knowsUsed=(used, total))

def infos():
    # set title
    response.title = 'Super Metroid Item Randomizer Solver'
    response.menu = [['Super Metroid Item Randomizer Solver', False, '#'],
                     ['Solve!', False, URL(f='solver')],
                     ['Information & Contact', True, URL(f='infos')]]

    return dict()
