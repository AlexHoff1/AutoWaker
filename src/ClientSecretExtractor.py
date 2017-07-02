import os

from ConfigHandler import getPath

def getClientSecret():
    relative_location = [getPath(), 'Data', 'ClientSecret.txt']
    fid = open(os.path.join(*relative_location))
    client_secret = fid.read()
    fid.close()
    return client_secret.strip()