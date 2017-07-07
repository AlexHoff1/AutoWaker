import logging
import os


LOG = logging.getLogger(name="autoWaker")

#  Writes the data to file, forcefullly.
def writeDataToFile(data = None, location = None):
    if location == '':
        LOG.info('location was empty.')
        return False
    try:
        LOG.info('Writing the data to a file.')
        out_file_opened = open(location, 'w')
        out_file_opened.write(data)
        out_file_opened.close()
        LOG.info('Successfully wrote data to file.')
        return True
            
    except IOError:
        LOG.info('Problem existed when writing the data, checking directory.')
        #Could be that the directory DNE
        directory = os.path.dirname(os.path.realpath(location))
        try:
            if not os.path.exists(directory):
                LOG.info('Directory did not exist. Creating directory.')
                os.makedirs(directory)
                out_file_opened = open(location, 'w')
                out_file_opened.write(data)
                out_file_opened.close()
                LOG.info('Successfully wrote data to file.')
                return True
        except:
            LOG.debug('Failed to write data to ' + str(location) + ' and the directory existed.')
            return False
#End writeDataToOutFile()
