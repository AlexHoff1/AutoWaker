import urllib2
import TokenGetter
import logging
import DataWriter as writer
LOG = logging.getLogger(name="autoWaker")

"""
  Used to query the API so we can get the data.
  
  To be implemented:
    getClientSecret() make it so that we don't hard code the client's secret >.>
    breaking the MakeAPICall() up.
    Logging
    
  Author: Alex Hoff
  License: ---
"""
class APIHandler():
    def __init__(self, ini_file, out_file, key_getter):
        self.ini_file_ = ini_file
        self.out_file_ = out_file
        self.key_getter_ = key_getter
        
    #  This makes an API call to retrieve data from fitbit.
    #  Returns:
    #   callSucceeded, callData
    #   callSucceeded - boolean that holds whether or not this call was  good.
    #   callData - the data returned from the call.
    def makeAPICall(self):
        #Start the request
        access_token, refresh_token = self.key_getter_.getTokens()
        LOG.info('The passed access_token to MakeAPICall is ' + str(access_token))
        req = urllib2.Request(self.ini_file_)
        
        #Add the access token in the header
        req.add_header('Authorization', 'Bearer ' + access_token)
        try:
            LOG.info('Trying to open the URL')
            response = urllib2.urlopen(req)
            LOG.info('Reading the response')
            full_response = response.read()
            writer.writeDataToFile(data = full_response, location = self.out_file_)
            LOG.info('Call to the URL succeeded.')
            
            return True, full_response
            
        # Catch errors, e.g. A 401 error that signifies the need for a new access token
        except urllib2.URLError as e:
            LOG.info('Call to the URL failed.')
            HTTPErrorMessage = e.read()
            LOG.info('ERROR message: \n   ' + str(HTTPErrorMessage))
            
            # See what the error was
            if (e.code == 401) and (HTTPErrorMessage.find("Access token expired") > 0):
                LOG.info('ERROR was out of date tokens, refreshing tokens.')
                access_token, refresh_token = self.key_getter_.getNewAccessToken(refresh_token)
                return self.makeAPICall(access_token, refresh_token)
            else:
                if(refresh_token!=None) and (HTTPErrorMessage.find("Refresh token invalid: ")):
                    LOG.info('Refresh token was invalid. Refreshing the tokens and running again.')
                    access_token, refresh_token = self.key_getter_.refreshTokens()
                return self.makeAPICall(access_token, refresh_token)
            # To implement: Catch other errors?
            LOG.info('ERROR was not out of date tokens, call failed.')
            return False, 'ERROR'
    #End MakeAPICall()
    
    #######CLASS VARIABLES#########
    key_getter_ = None
    ini_file_ = None
    out_file_ = None
    #######CLASS VARIABLES#########

#End APIHandler class