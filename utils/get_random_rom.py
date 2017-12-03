#!/usr/bin/python3

# the html form on the randomizer website:
#    <form method="post" action="/randomize" enctype="multipart/form-data">        
#    <div class="form-group">
#        <label for="filename">Pick a vanilla (unheadered) SM ROM to upload and patch</label>
#        <input type="file" id="filename" name="filename"/>
#    </div>
#    <div class="form-group">
#        <label for="seed">Enter a seed here or leave it at 0 to create a new random seed:</label>
#        <input type="text" id="seed" name="seed" value="0" class="form-control" />
#    </div>
#    <div class="form-group">
#        <label for="difficulty">Difficulty:</label>
#        <select name="difficulty" id="difficulty" class="form-control">
#          <option value="0">Casual</option>
#          <option value="1" selected>Normal</option>
#          <option value="2">Hard</option>
#          <option value="3">Tournament</option>
#          <option value="4">Open Mode</option>
#        </select>
#    </div>
#    <input type="submit" value="Randomize!" class="btn btn-primary"/>
#    </form>

import requests, shutil, random

def getRandomizedRom(originalRomFilePath, seed):
    # generate a new Tournament random rom by uploading a rom to the website
    # and downloading the generated one

    url = 'https://itemrando.supermetroid.run/randomize'

    session = requests.session()
    r = session.get(url)

    # difficulty 3 is Tournament
    data = [('seed', seed), ('difficulty', 3)]
    files = {'filename': (originalRomFilePath,
                          open(originalRomFilePath, 'rb'),
                          'application/octet-stream')}

    r2 = session.post(url, data=data, files=files, stream=True)

    if r2.status_code == 200:
        # in the reponse we have the headers variable containing the generated seed:
        # 'headers': {'Content-Length': '1576728', 
        #            'Content-Encoding': 'gzip', 
        #            'Keep-Alive': 'timeout=5, max=99', 
        #            'Content-Type': 'application/octet-stream', 
        #            'Content-Disposition': 'attachment; filename="Item Randomizer TX9255788.sfc"', 
        #            'Server': 'Suave (https://suave.io)', 
        #            'Connection': 'Keep-Alive', 'Date': 'Sun, 05 Nov 2017 12:12:15 GMT'},
        outRomFileName = r2.headers['Content-Disposition'][len('attachment; filename="'):-len('"')]

        with open(outRomFileName, 'wb') as f:
            r2.raw.decode_content = True
            shutil.copyfileobj(r2.raw, f)
        return outRomFileName
    else:
        print("An error happened: {}".format(r2.status_code))
        return None

if __name__ == "__main__":
    random.seed()
    fileName = getRandomizedRom('Super_Metroid_JU.smc', random.randint(0, 9999999))
    print("The randomized rom file is \"{}\"".format(fileName))
