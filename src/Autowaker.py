import sys
import time
import TokenGetter
import APIHandler
import DataHandler
import wakeUpCaller
import datetime
import logging



today = time.strftime("%Y-%m-%d")
#This is the Fitbit URL to use for the API call
FitbitURLBase = "https://api.fitbit.com/1/user/-/sleep/date/"
FitbitURL = FitbitURLBase + today + ".json"

#Use this URL to refresh the access token
TokenURL = "https://api.fitbit.com/oauth2/token"

#Get and write the tokens from here
IniFile = r"C:\Users\Owner\Documents\Code\tokens.txt"
OutFile = r"C:\Users\Owner\Documents\Code\AutoWaker\Data\MyData"  + today + ".txt"

#Some contants defining API error handling responses
TokenRefreshedOK = "Token refreshed OK"
ErrorInAPI = "Error when making API call that I couldn't handle"


def main(): 
    
    LOG = setupLogger()
    LOG.info('STARTING')
    
    # wait until we should start. Make this into a class or method?
    while datetime.datetime.now().time()>datetime.time(3,0,0,0) or datetime.datetime.now().time()<datetime.time(2,0,0,0):
        LOG.info('Pinging every 120 seconds to check if the person should be asleep.')
        time.sleep(120)
    
    key_getter = TokenGetter.TokenGetter(IniFile)
        
    #Get the config
    access_token, refresh_token = key_getter.getTokens()
    api_handler = APIHandler.APIHandler(FitbitURL, OutFile, key_getter)
    data_handler = DataHandler.DataHandler()
    
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
            time.sleep(600)  #Check every 10 minutes.
            APICallOK, APIResponse = api_handler.makeAPICall()
            if not APICallOK:
                return -1
            sleeping, start_time = data_handler.getSleepStartTime(APIResponse)
        
        #Sleeping is true now.
        LOG.info('You started sleeping at ' + str(start_time) + ' today.')
        wake_up = wakeUpCaller.wakeUpCaller()
        wake_up.callWake(start_time)
        
def setupLogger():
    logging.basicConfig(filename='sleepDataLogs.log',level=logging.INFO, filemode ='w')
    hdlr = logging.FileHandler(r'C:\Users\Owner\Desktop\Code\AutoWaker\Logs\sleepLogs' + today + '.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    hdlr.setLevel(logging.INFO)
    LOG = logging.getLogger(name = "autoWaker")
    LOG.addHandler(hdlr)
    LOG.setLevel(logging.INFO)
    return LOG

if __name__ == '__main__':
    main()