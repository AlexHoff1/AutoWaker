import logging
import os
import sys

from APIHandler import APIHandler
from ConfigHandler import getPath
from DataHandler import DataHandler
from LogCreator import setupLogger
from SleepChecker import SleepChecker
from TimeHandler import today, now, startCheckTime, endCheckTime, stallAction
from TokenGetter import TokenGetter
from WakeUpCaller import WakeUpCaller


#Set the proper path
os.chdir(getPath())

today_as_dt = today()


#Get and write the tokens from here
s = [getPath(), 'Data', 'MyData_' + today_as_dt + '.txt']
OutFile = os.path.join(*s)

class ServerRequestHandler():
    def __init__(self, user = None, date = None):
        self.user_ = user
        self.date_ = date
        
    def getUser(self):
        return self.user_
    
    
    def getWakeTime(self): 
        user = self.getUser()
        FitbitURL = "https://api.fitbit.com/1/user/" + user + "/sleep/date/" + today_as_dt + ".json"
        LOG = setupLogger()
        LOG.info('STARTING')
        key_getter_location = os.path.join(getPath(),'Tokens.txt')
        print key_getter_location

        key_getter = TokenGetter(key_getter_location)
        api_handler = APIHandler(FitbitURL, OutFile, key_getter)
        data_handler = DataHandler()
        
        #Make the API call
        APIResponse = api_handler.cancelIfAPICallBad()
        sleep_checker = SleepChecker(OutFile)
        LOG.info("Checking if the user is asleep.")
        if sleep_checker.isAwake():
            LOG.info("User is still awake.")
            return '06:00:00'
        else:
            APIResponse = api_handler.cancelIfAPICallBad()
            sleeping, start_time = data_handler.getSleepStartTime(APIResponse)
            
        #Sleeping is true now.
        LOG.info('You started sleeping at ' + str(start_time) + ' today.')
        wake_up = WakeUpCaller()
        return wake_up.calculateWakeTime(start_time);