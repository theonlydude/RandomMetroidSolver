import os, json, urllib, re, math, base64, string, random

from web.backend.utils import raiseHttp
from rom.ips import IPS_Patch
from utils.db import DB

from gluon.validators import IS_LENGTH, IS_MATCH, IS_INT_IN_RANGE

# discord webhook for plandorepo
try:
    from webhook import webhookUrl
    from discord_webhook import DiscordWebhook, DiscordEmbed
    webhookAvailable = True
except:
    webhookAvailable = False


ipsBasePath = "plandository/"
class PlandoRepo(object):
    def __init__(self, request):
        self.request = request
        self.vars = self.request.vars

    def run(self):
        with DB() as db:
            url = self.request.env.request_uri.split('/')
            msg = ""
            plandos = []
            expand = True
            if len(url) > 0 and url[-1] != 'plandorepo':
                # a plando name was passed as parameter
                plandoName = url[-1]

                # decode url
                plandoName = urllib.parse.unquote(plandoName)

                # sanity check
                if IS_MATCH('^[a-zA-Z0-9 -_]*$')(plandoName)[1] is not None:
                    msg = "Plando name can only contain [a-zA-Z0-9 -_]"
                else:
                    plandos = db.getPlando(plandoName)
                    if plandos is None or len(plandos) == 0:
                        msg = "Plando not found"
            if plandos is None or len(plandos) == 0:
                # get plando list
                plandos = db.getPlandos()
                expand = False

        return dict(plandos=plandos, msg=msg, expand=expand, math=math, re=re)

    def plandoRateWebService(self):
        if self.vars.plando == None:
            raiseHttp(400, "Missing parameter plando")
        plando = self.vars.plando

        if self.vars.rate == None:
            raiseHttp(400, "Missing parameter rate")
        rate = self.vars.rate

        if IS_LENGTH(maxsize=32, minsize=1)(plando)[1] is not None:
            raiseHttp(400, "Plando name must be between 1 and 32 characters")

        if IS_MATCH('^[a-zA-Z0-9 -_]*$')(plando)[1] is not None:
            raiseHttp(400, "Plando name can only contain [a-zA-Z0-9 -_]")

        if IS_INT_IN_RANGE(1, 6)(rate)[1] is not None:
            raiseHttp(400, "Rate name must be between 1 and 5")
        rate = int(rate)
        ip = self.request.client

        with DB() as db:
            db.addRating(plando, rate, ip)
            newRate = db.getPlandoRate(plando)
        if newRate == None:
            raiseHttp(400, "Can't get new rate")
        newCount = newRate[0][0]
        newRate = float(newRate[0][1])
        data = {
            "msg": "",
            "purePlandoName": re.sub('[\W_]+', '', plando),
            "rate": newRate,
            "count": newCount
        }
        return json.dumps(data)

    def downloadPlandoWebService(self):
        if self.vars.plando is None:
            raiseHttp(400, "Missing parameter plando")
        plandoName = self.vars.plando

        if IS_LENGTH(maxsize=32, minsize=1)(plandoName)[1] is not None:
            raiseHttp(400, "Plando name must be between 1 and 32 characters")

        if IS_MATCH('^[a-zA-Z0-9 -_]*$')(plandoName)[1] is not None:
            raiseHttp(400, "Plando name can only contain [a-zA-Z0-9 -_]")

        ipsFileName = os.path.join(ipsBasePath, "{}.ips".format(plandoName))
        if not os.path.isfile(ipsFileName):
            raiseHttp(400, "Plando ips not found on server")

        with open(ipsFileName, 'rb') as ipsFile:
            ipsData = ipsFile.read()

        with DB() as db:
            maxSize = db.getPlandoIpsMaxSize(plandoName)
            db.increaseDownloadCount(plandoName)

        data = {
            "ips": base64.b64encode(ipsData).decode(),
            "fileName": "{}.sfc".format(plandoName),
            "maxSize": maxSize
        }

        return json.dumps(data)

    def removeHtmlTags(self, text):
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def generateUpdateKey(self):
        # 8 chars string
        stringLength = 8
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(stringLength))

    def handleIps(self, plandoName, romDataJson):
        romDataJson = self.vars.romData
        romDataRaw = json.loads(romDataJson)
        # everything is string in json, cast to int
        romData = {}
        for addr in romDataRaw:
            romData[int(addr)] = int(romDataRaw[addr])

        # dict: address -> value, transform it dict: address -> [values]
        ipsData = {}
        prevAddr = -0xff
        curRecord = []
        curRecordAddr = -1
        for addr in sorted(romData):
            if addr == prevAddr + 1:
                curRecord.append(romData[addr])
            else:
                if len(curRecord) > 0:
                    # save current record
                    ipsData[curRecordAddr] = bytearray(curRecord)
                # start a new one
                curRecordAddr = addr
                curRecord = [romData[addr]]
            prevAddr = addr
        # save last record
        ipsData[curRecordAddr] = bytearray(curRecord)

        # generate ips using the records
        ipsPatch = IPS_Patch(ipsData)
        maxSize = ipsPatch.max_size

        # store ips in the repository
        ipsPatch.save(os.path.join(ipsBasePath, "{}.ips".format(plandoName)))

        return maxSize

    def uploadPlandoWebService(self):
        with DB() as db:
            count = db.getPlandoCount()
            plandoLimit = 2048
            if count is None or count[0][0] >= plandoLimit:
                raiseHttp(400, "Maximum number of plandos reach: {}".format(plandoLimit))

        for param in ["author", "plandoName", "longDesc", "preset", "romData"]:
            if self.vars[param] == None:
                raiseHttp(400, "Missing parameter {}".format(param))

        for param in ["author", "plandoName", "preset"]:
            if IS_LENGTH(maxsize=32, minsize=1)(self.vars[param])[1] is not None:
                raiseHttp(400, "{} must be between 1 and 32 characters".format(param))

        for param in ["longDesc"]:
            if IS_LENGTH(maxsize=2048, minsize=1)(self.vars[param])[1] is not None:
                raiseHttp(400, "{} must be between 1 and 2048 characters".format(param))

        plandoName = self.vars.plandoName
        if IS_MATCH('^[a-zA-Z0-9 -_]*$')(plandoName)[1] is not None:
            raiseHttp(400, "Plando name can only contain [a-zA-Z0-9 -_]")

        # check if plando doesn't already exist
        with DB() as db:
            check = db.checkPlando(plandoName)

        if check is not None and len(check) > 0 and check[0][0] == plandoName:
            raiseHttp(400, "Can't create plando, a plando with the same name already exists")

        author = self.vars.author
        longDesc = self.removeHtmlTags(self.vars.longDesc)
        preset = self.vars.preset

        maxSize = self.handleIps(plandoName, self.vars.romData)

        updateKey = self.generateUpdateKey()

        with DB() as db:
            db.insertPlando((plandoName, author, longDesc, preset, updateKey, maxSize))

        if webhookAvailable:
            self.plandoWebhook(plandoName, author, preset, longDesc)

        return json.dumps(updateKey)

    def plandoWebhook(self, plandoName, author, preset, longDesc):
        webhook = DiscordWebhook(url=webhookUrl, username="Plandository")

        embed = DiscordEmbed(title=plandoName, description="New {} plando by {}".format(preset, author), color=242424)

        # there's a limit for discord for the size of an embed field
        embedLimit = 512
        if len(longDesc) > embedLimit:
            longDesc = longDesc[:embedLimit]+"..."
        embed.add_embed_field(name="description", value=longDesc, inline=False)

        permalink = self.getPermalink(plandoName)
        embed.add_embed_field(name="permalink", value=permalink)
        webhook.add_embed(embed)

        try:
            response = webhook.execute()
        except:
            pass

    def getPermalink(self, plandoName):
        return "http://{}/plandorepo/{}".format(self.request.env.HTTP_HOST, urllib.parse.quote(plandoName))

    def deletePlandoWebService(self):
        for param in ["plandoName", "plandoKey"]:
            if self.vars[param] == None:
                raiseHttp(400, "Missing parameter {}".format(param))

        plandoName = self.vars.plandoName
        plandoKey = self.vars.plandoKey

        if IS_LENGTH(maxsize=32, minsize=1)(plandoName)[1] is not None:
            raiseHttp(400, "Plando name must be between 1 and 32 characters")
        if IS_MATCH('^[a-zA-Z0-9 -_]*$')(plandoName)[1] is not None:
            raiseHttp(400, "Plando name can only contain [a-zA-Z0-9 -_]")

        if IS_LENGTH(maxsize=8, minsize=1)(plandoKey)[1] is not None:
            raiseHttp(400, "Plando key must be between 1 and 8 characters")
        if IS_MATCH('^[a-zA-Z0-9]*$')(plandoKey)[1] is not None:
            raiseHttp(400, "Plando key can only contain [a-zA-Z0-9]")

        with DB() as db:
            valid = db.isValidPlandoKey(plandoName, plandoKey)
            if valid is None or len(valid) == 0:
                raiseHttp(400, "Plando key mismatch")
            db.deletePlandoRating(plandoName)
            db.deletePlando(plandoName)

        return json.dumps("Plando {} deleted".format(plandoName))

    def updatePlandoWebService(self):
        for param in ["author", "plandoName", "longDesc", "preset", "plandoKey"]:
            if self.vars[param] == None:
                raiseHttp(400, "Missing parameter {}".format(param))

        for param in ["author", "plandoName", "preset"]:
            if IS_LENGTH(maxsize=32, minsize=1)(self.vars[param])[1] is not None:
                raiseHttp(400, "{} must be between 1 and 32 characters".format(param))

        for param in ["plandoKey"]:
            if IS_LENGTH(maxsize=8, minsize=1)(self.vars[param])[1] is not None:
                raiseHttp(400, "{} must be between 1 and 8 characters".format(param))

        for param in ["longDesc"]:
            if IS_LENGTH(maxsize=2048, minsize=1)(self.vars[param])[1] is not None:
                raiseHttp(400, "{} must be between 1 and 2048 characters".format(param))

        plandoName = self.vars.plandoName
        if IS_MATCH('^[a-zA-Z0-9 -_]*$')(plandoName)[1] is not None:
            raiseHttp(400, "Plando name can only contain [a-zA-Z0-9 -_]")

        author = self.vars.author
        longDesc = self.removeHtmlTags(self.vars.longDesc)
        preset = self.vars.preset
        plandoKey = self.vars.plandoKey

        # check update key
        with DB() as db:
            valid = db.isValidPlandoKey(plandoName, plandoKey)
            if valid is None or len(valid) == 0:
                raiseHttp(400, "Plando key mismatch")

            if self.vars.romData is not None:
                print("updatePlandoWebService: update ips")
                maxSize = self.handleIps(plandoName, self.vars.romData)
                db.updatePlandoAll((author, longDesc, preset, maxSize, plandoName))
            else:
                db.updatePlandoMeta((author, longDesc, preset, plandoName))

        return json.dumps("Plando {} updated succesfully.".format(plandoName))
