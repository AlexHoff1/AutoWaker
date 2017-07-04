import logging
import os
import sys

from APIHandler import APIHandler
from ConfigHandler import getPath
from DataHandler import DataHandler
from TimeHandler import today, now, startCheckTime, endCheckTime, stallAction
from TokenGetter import TokenGetter
from WakeUpCaller import WakeUpCaller


#Set the proper path
os.chdir(getPath())

today_as_dt = today()
#This is the Fitbit URL to use for the API call
FitbitURL = "https://api.fitbit.com/1/user/-/sleep/date/" + today_as_dt + ".json"

#Get and write the tokens from here
s = [getPath(), 'Data', 'MyData_' + today_as_dt + '.txt']
OutFile = os.path.join(*s)

#Some contants defining API error handling responses
TokenRefreshedOK = "Token refreshed OK"
ErrorInAPI = "Error when making API call that I couldn't handle"


def main(): 
    
    LOG = setupLogger()
    LOG.info('STARTING')
    
    # wait until we should start. Make this into a class or method?
    while now()>endCheckTime() or now()<startCheckTime():
        LOG.info('Pinging every 120 seconds to check if the person should be asleep.')
        stallAction(120)
    
    key_getter = TokenGetter(os.path.join(getPath(),'tokens.txt'))
        
    #Get the config
    access_token, refresh_token = key_getter.getTokens()
    api_handler = APIHandler(FitbitURL, OutFile, key_getter)
    data_handler = DataHandler()
    
    #Make the API call
    APICallOK, APIResponse = api_handler.makeAPICall()
    if not APICallOK:
        return -1
    
    LOG.info('starting the cycle... Forever.')
    while True:
        sys.stdout.flush()
        data = data_handler.getData(OutFile)
        sleeping, start_time = data_handler.getSleepStartTime(data)
        while not sleeping:
            LOG.info('still not asleep I see...')
            sys.stdout.flush()
            stallAction(600)  #Check every 10 minutes.
            APICallOK, APIResponse = api_handler.makeAPICall()
            if not APICallOK:
                return -1
            sleeping, start_time = data_handler.getSleepStartTime(APIResponse)
        
        #Sleeping is true now.
        LOG.info('You started sleeping at ' + str(start_time) + ' today.')
        wake_up = WakeUpCaller()
        wake_up.callWake(start_time)
        
def setupLogger():
    logging.basicConfig(filename='sleepDataLogs.log',level=logging.INFO, filemode ='w')
    relative_log_location = [getPath(), 'Logs', 'sleepLogs' + today_as_dt + '.log']
    hdlr = logging.FileHandler(os.path.join(*relative_log_location))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    hdlr.setLevel(logging.INFO)
    LOG = logging.getLogger(name = "autoWaker")
    LOG.addHandler(hdlr)
    LOG.setLevel(logging.INFO)
    return LOG

if __name__ == '__main__':
    main()