# check if gdrive is available
try:
    # installation of gdrive client:
    # https://developers.google.com/drive/api/v3/quickstart/python
    # pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    import pickle, os, base64, shutil

    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request

    from gdrive_params import gdriveParams
    gdriveAvailable = True
except:
    gdriveAvailable = False

baseDir = 'ips_repo'

class GDrive(object):
    def __init__(self):
        self.gdriveAvailable = gdriveAvailable
        if self.gdriveAvailable == False:
            return

        try:
            # auth
            # If modifying these scopes, delete the file token.pickle.
            SCOPES = ['https://www.googleapis.com/auth/drive']
            creds = None
            # The file token.pickle stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)

            self.drive_service = build('drive', 'v3', credentials=creds, cache_discovery=False)
        except Exception as e:
            print("GDrive.__init__::error: {}".format(e))
            self.gdriveAvailable = False

    def createRemoteFolder(self, folderName):
        # Create a folder on Drive, returns the newely created folders ID
        body = {
          'name': folderName,
          'mimeType': "application/vnd.google-apps.folder"
        }
        body['parents'] = [gdriveParams['dirIds'][gdriveParams['baseDir']]]
        root_folder = self.drive_service.files().create(body = body).execute()
        return root_folder['id']

    def upload(self, key, fileName, ipsData):
        print("GDrive.upload: key: {} filename: {}".format(key, fileName))

        if self.gdriveAvailable == False:
            return False

        try:
            # create directory to localy store the ips
            ipsDir = os.path.join(baseDir, str(key))
            os.makedirs(ipsDir, mode=0o755, exist_ok=True)

            # extract ipsData
            ips = base64.b64decode(ipsData)

            # update ips as key/fileName.ips
            ipsFileName = fileName.replace('sfc', 'ips')
            ipsLocal = os.path.join(ipsDir, ipsFileName)
            with open(ipsLocal, 'wb') as f:
                f.write(ips)

            # create remote key folder and upload ips
            newDirId = self.createRemoteFolder(str(key))
            file_metadata = {'name': ipsFileName, 'parents': [newDirId]}

            media = MediaFileUpload(ipsLocal, mimetype='application/octet-stream')
            file = self.drive_service.files().create(body=file_metadata,
                                                     media_body=media,
                                                     fields='id').execute()

            # delete local directory
            shutil.rmtree(ipsDir)

            print("GDrive.upload::success")

            return True
        except Exception as e:
            print("GDrive.upload::error: {}".format(e))
            self.gdriveAvailable = False
            return False

    def download(self, key):
        # return fileName.ips
        if self.gdriveAvailable == False:
            return None

        # list file in key directory
        ipsDir = os.path.join(baseDir, gdriveParams['baseDir'], str(key))
        ipsFile = os.listdir(ipsDir)

        # download it
        with open(ipsFile, 'rb') as f:
            ips = f.read()
        ips = base64.b64encode(ips).decode()
        return ips
