import os

from ConfigHandler import getPath

def getClientSecret():
    relative_location = [getPath(), 'Data', 'ClientSecret.txt']
    try:
        fid = open(os.path.join(*relative_location))
        client_secret = fid.read()
        fid.close()
    except:
        raise IOError('The client secret file did not exist.')
    return client_secret.strip()