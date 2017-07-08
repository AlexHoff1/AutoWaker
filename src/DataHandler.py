import datetime
import json
import logging

LOG = logging.getLogger(name="autoWaker")

"""
  Used to manage the data once the API handler has sent it.
  
  To be implemented:
      getSleepEndTime()  #Would clean up the code.
    
  Author: Alex Hoff
  License: ---
"""
class DataHandler():
    def __init__(self):
        None
                
    #  Reads the OutFile to get the data.
    #  Returns the contents of the file
    #  Throws IOError if anything fails.
    def getData(self, out_file = None):
        if type(out_file)!=str or out_file == '':
            return ''  # Theres' no data in it after all
        LOG.info('Opening the file: ' + str(out_file))
        try:
            File = open(out_file, 'r')
            LOG.info('Reading from the file')
            data = File.read()
            LOG.info('Closing the file.')
            File.close()
            return data
            
        except:
            LOG.error('Problem getting the data from: ' + str(out_file))
            raise IOError, str(out_file) + ' failed to read.'
    #End getData()
    
    #  Extract the start time from the data.
    #  Returns:
    #   isAsleep, startTime
    #   isAsleep is True if the person is still sleeping as far as the data is concerned.
    #   startTime is the time that sleep started (whether or not they're awake)
    def getSleepStartTime(self, data = None):
        if type(data)!=str:
            return False, False
        try:
            awake = self.isAwakeInData(data)
            if (awake):
                return False, None
                
            LOG.info('Trying to extract the start time from the data.')
            response_json = json.loads(data)
            start_time_str = str(response_json['summary']['startTime'])
            start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S.%f')
            LOG.info('Start time: ' + start_time_str)
            LOG.info('Person has started sleeping today, and hasn\'t woken up.')
            return True, start_time
            
        except ValueError:
            LOG.info('Person hasn\'t started sleeping yet.')
            return False, False
        except:
            LOG.error('Error extracting the time from ' + start_time_str)
            return False, False
    #End getSleepStartTime()
    
    #  Returns a boolean indicating whether or not the person is still asleep
    def isAwakeInData(self, data = None):
        if type(data)!=str:
            return True
        try:
            LOG.info('Trying to see whether the person has already woken up.')
            response_json = json.loads(data)
            end_time_str = str(response_json['summary']['endTime'])
            
            #This weird datetime.datetime thing is how the library works unfortunately.
            end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S.%f')
            if (end_time!=None):
                LOG.info('Sleep ended at ' + end_time_str)
                return True
            else:
                LOG.info('Sleep has not yet ended.')
                return False
            
        except ValueError:
            LOG.info('Sleep has not yet ended.')
            return False
        except:
            LOG.error('Error extracting the time from ' + end_time_str)
            return False, False
    #End isAWakeInData()

#End dataHandler class