import base64
import json
import logging
import urllib
import urllib2

from ClientSecretExtractor import getClientSecret

LOG = logging.getLogger(name="autoWaker")

#From the developer site
OAuthTwoClientID = "228FD6"
ClientOrConsumerSecret = getClientSecret()

#Will need to change that...
"""
  Used to get and refresh the Tokens so we can get the data.
  
  To be implemented:
    getClientSecret() make it so that we don't hard code the client's secret >.>
    Proper and consistent naming.
    Logging
    
  Author: Alex Hoff
  License: ---
"""
class TokenGetter():
    def __init__(self, config_file):
        self.token_loc_ = config_file
        
    #  Get the config from the config file. This is the access and refresh tokens
    def getTokens(self):
        LOG.info('Trying to open the file containing the Tokens.')
        try:
            file_obj = open(self.token_loc_, 'r')
            LOG.info('Trying to retrieve the data. Opened file successfully.')
            access_token, refresh_token = file_obj.read().splitlines()
        except:
            LOG.debug('current token file ' + str(self.token_loc_) + ' is invalid.')
            raise IOError
        
        #Read first two lines - first is the access token, second is the refresh token
        file_obj.close()
        LOG.info('Successfully closed the file that contains current tokens.')
        
        #Return values
        return access_token, refresh_token
    #END getTokens()
    
    
    #  Writes the new tokens to the file.
    def setTokens(self, access_token, refresh_token):
        LOG.info("Writing new tokens to the config file")
        LOG.info("Writing this: " + access_token + " and " + refresh_token)
        
        if (access_token==None or refresh_token==None):
            LOG.debug('At least one token passed was none type. Check the rest of the logs for errors.')
            raise IOError
        try:
            self.copyOld()
            file_obj = open(self.token_loc_, 'w')  #NOTE: This deletes old file!
            file_obj.write(access_token + "\n" + refresh_token)
            file_obj.close()
            
        except:
            LOG.debug('Problem: FileObj didn\'t properly write the tokens!')
            #forceWrite(self.token_loc_, access_token, refresh_token)
    #END setTokens()
    
    
    #  Writes the new tokens to a file and returns them.
    def refreshTokens(self):
        access_token, refresh_token = self.getTokens()
        self.setTokens(access_token, refresh_token)
        access_token, refresh_token = self.getNewAccessToken(refresh_token)
        if (access_token == None):
            #If it returns None then there's an unhandled error somewhere.
            #Probably the refresh key being invalid entirely.
            LOG.debug('Refresh key probably invalid. No new tokens retrieved.')
            LOG.debug('Returning None, None')
            return None, None
        else:
            self.setTokens(access_token, refresh_token)
            return access_token, refresh_token
    
    #END refreshTokens()
    
    
    #  Make a HTTP POST to get a new refresh token and access token.
    def getNewAccessToken(self, refresh_token):
        LOG.info('Refresh token: ' + str(refresh_token))
        #Form the data payload
        body_text = {'grant_type' : 'refresh_token',
                    'refresh_token' : refresh_token}
        #URL Encode it
        BodyURLEncoded = urllib.urlencode(body_text)
        
        #Start the request
        tokenreq = urllib2.Request(self.token_url_, BodyURLEncoded)
        
        #Add the headers, first we base64 encode the client id and 
        #client secret with a : inbetween and create the authorisation header
        tokenreq.add_header('Authorization', 'Basic ' + base64.b64encode(OAuthTwoClientID + ":" + ClientOrConsumerSecret))
        tokenreq.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        #Fire off the request
        try:
            token_response = urllib2.urlopen(tokenreq)
            #See what we got back.  If it's this part of  the code it was OK
            full_response = token_response.read()
        
            #Need to pick out the access token and write it to the config file. 
            #Use a JSON manipluation module to accomplish this.
            response_json = json.loads(full_response)
        
            #Read the access token as a string
            new_access_token = str(response_json['access_token'])
            new_refresh_token = str(response_json['refresh_token'])
            self.setTokens(new_access_token, new_refresh_token)

            #Return the new tokens to be written or used.
            return new_access_token, new_refresh_token
        
        except urllib2.URLError as e:
            LOG.info("An error was raised when getting the access token.  Need to stop here")
            LOG.error(e.read())
            #If this happens at a bad time it might go pretty bad.
            #Some robust recovery should be added into this.
            return None, None
    #END getNewAccessToken()

    #Copy the old tokens to a temp file, just in case.
    def copyOld(self):
        access_token, refresh_token = self.getTokens()
        
        #Temp location to write to
        try:
            fid = open('./tempOldTokens','w')
            fid.write(access_token + "\n" + refresh_token)
            fid.close()
        except:
            LOG.warning("Writing to temporary file failed.")
    #END copyOld()
    
    ############CLASS VARIABLES##############
    token_loc_ = ''
    token_url_ = "https://api.fitbit.com/oauth2/token"
    ############CLASS VARIABLES##############

#END TokenGetter class