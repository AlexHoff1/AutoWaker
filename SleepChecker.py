import DataHandler
"""




"""
class SleepChecker():
    def __init__(self, data_location):
        self.data_location_ = data_location
        
    def isAsleep(self):
        try:
            file_opened = open(self.data_location_)
            data = file_opened.read()
            file_opened.close()
            
            data_handler = DataHandler.DataHandler()
            isAsleep, _ = data_handler.getSleepStartTime(data)
            return isAsleep
        except:
            return False
        return False
    
    def isAwake(self):
        return not self.isAsleep()
        
    ######CLASS VARIABLES#######
    data_location_ = ''
    ######CLASS VARIABLES#######

#END SleepChecker