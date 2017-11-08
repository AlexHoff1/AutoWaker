import logging
import os

from ConfigHandler import getPath

LOG = logging.getLogger(name="autoWaker")

def getClientSecret():
    relative_location = [getPath(), 'Data', 'ClientSecret.txt']
    try:
        fid = open(os.path.join(*relative_location))
        client_secret = fid.read()
        fid.close()
    except:
        LOG.error('The client secret file did not exist.')
        raise IOError('The client secret file did not exist.')
    
    LOG.info('Successfully extracted the client secret.')
    return client_secret.strip()