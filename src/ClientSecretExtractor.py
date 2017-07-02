import os

import ConfigHandler

def getClientSecret():
    relative_location = [ConfigHandler.getPath(), 'Data', 'ClientSecret.txt']
    fid = open(os.path.join(*relative_location))
    client_secret = fid.read()
    fid.close()
    return client_secret.strip()