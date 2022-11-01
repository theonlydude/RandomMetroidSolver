#!/usr/bin/python3
# call the remote webservice in cli mode instead of generating the seed localy.
# three parameters are mandatory:
#  --skillPreset: the skill preset file (~/RandomMetroidSolver/standard_presets/*.json)
#  --randoPreset: the rando preset file (~/RandomMetroidSolver/rando_presets/*.json)
#  --rom: the vanilla ROM file
# for your tests please use your local web2py installation (--remoteUrl local) or the beta website (--remoteUrl beta).

import json, argparse, sys, random, os, os.path, base64, shutil, tempfile
from requests import Session
from rom.rom import RealROM
from rom.ips import IPS_Patch
from logic.logic import Logic
from utils.utils import getRandomizerDefaultParameters

if __name__ == "__main__":
    Logic.factory('vanilla')

    parser = argparse.ArgumentParser(description="Random Metroid Randomizer webservice client")
    parser.add_argument('--skillPreset', help="skill preset file", dest='skillPreset', nargs='?', default=None)
    parser.add_argument('--rom', help="vanilla ROM file", dest='rom', nargs='?', default=None)
    parser.add_argument('--randoPreset', help="rando preset file", dest="randoPreset", nargs='?', default=None)
    parser.add_argument('--seed', help="seed number (optional)", dest="seed", nargs='?', default=0, type=int)
    parser.add_argument('--remoteUrl', help="remote url to connect to", dest="remoteUrl", nargs='?', default='local', choices=['local', 'beta', 'production'])
    parser.add_argument('--port', help="custom port", dest='port', nargs='?', default=8000)

    # parse args
    args = parser.parse_args()

    if args.skillPreset == None or args.rom == None or args.randoPreset == None:
        parser.print_help()
        sys.exit(-1)

    # load rando preset
    with open(args.randoPreset) as randoPresetFile:
        randoParams = json.load(randoPresetFile)

    # load skill preset (path/to/file/preset.json)
    (preset, ext) = os.path.splitext(os.path.split(args.skillPreset)[-1])

    # we send the content of the skill preset instead of its name (for historical reasons)
    with open(args.skillPreset) as skillPresetFile:
        randoParams["paramsFileTarget"] = skillPresetFile.read()

    randoParams["preset"] = preset
    if args.seed == 0:
        randoParams["seed"] = random.randrange(sys.maxsize)
    else:
        randoParams["seed"] = args.seed

    # not all parameters are present in rando preset, add default value for missing ones
    defaultParams = getRandomizerDefaultParameters()

    for (key, value) in defaultParams.items():
        if key not in randoParams:
            randoParams[key] = value

    # fix multiselect parameters for rando webservice
    # (it expects a string '"x1","x2"' when a pool of multiple values are available to randomize)
    for param in randoParams:
        if type(randoParams[param]) == list:
            randoParams[param] = ','.join(randoParams[param])

    # call web service
    if args.remoteUrl == 'local':
        baseUrl = 'http://127.0.0.1:{}/'.format(args.port)
    elif args.remoteUrl == 'beta':
        baseUrl = 'http://variabeta.pythonanywhere.com/'
    elif args.remoteUrl == 'production':
        baseUrl = 'http://randommetroidsolver.pythonanywhere.com/'
    randoUrl = baseUrl + 'randomizer'
    webServUrl = baseUrl + 'randomizerWebService'

    # HEAD requests ask for *just* the headers, which is all we need to grab the session cookie
    session = Session()
    session.head(randoUrl)

    response = session.post(
        url=webServUrl,
        data=randoParams,
        headers={
            'Referer': randoUrl
        }
    )

    # check that we don't have errors
    if response.status_code != 200:
        print("An error {} occured when calling the randomizer webservice. Error: {}".format(response.status_code, response.content))
        exit(-1)

    # the output is a dict
    data = eval(response.text)

    if data.get('status') == 'NOK':
        print("An error occured when calling the randomizer webservice. Error: {}".format(data.get('errorMsg')))
        exit(-1)

    # generate randomized rom
    romFileName = args.rom
    outFileName = data["fileName"]
    shutil.copyfile(romFileName, outFileName)
    romFile = RealROM(outFileName)

    ipsData = data["ips"]
    ipsData = base64.b64decode(ipsData.encode('ascii'))

    # our ips patcher need a file (or a dict), not the content of the ips file
    (fd, ipsFileName) = tempfile.mkstemp()
    os.close(fd)

    with open(ipsFileName, 'wb+') as ipsFile:
        ipsFile.write(ipsData)

    romFile.ipsPatch([IPS_Patch.load(ipsFileName)])

    os.remove(ipsFileName)
        
    # write dest rom
    romFile.close()

    print("permalink: {}/customizer/{}".format(baseUrl, data["seedKey"]))

    print("additional message: {}".format(data["errorMsg"]))
    print("{} generated succesfully".format(outFileName))
