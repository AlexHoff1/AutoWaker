import DataHandler
"""
    SleepChecker simply summarizes the methods of returning whether or not
    a person is actually asleep. This is just a nicer way to get this info
    when it is needed.

    Takes: Location of the data

    Author: Alex Hoff
    License: ---
"""
class SleepChecker():
    def __init__(self, data_location):
        self.data_location_ = data_location
        
    
    def isAsleep(self):
        try:
            data_handler = DataHandler.DataHandler()
            is_asleep, _ = data_handler.getSleepStartTime(data_handler.getData(self.data_location_))
            return is_asleep
        except:
            return False
        return False
    
    def isAwake(self):
        return not self.isAsleep()
        
    ######CLASS VARIABLES#######
    data_location_ = ''
    ######CLASS VARIABLES#######

#END SleepChecker