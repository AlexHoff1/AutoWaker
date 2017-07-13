import base64
import json
import logging
import urllib
import urllib2
import pymysql

from ClientSecretExtractor import getClientSecret

LOG = logging.getLogger(name="autoWaker")

#From the developer site
OAuthTwoClientID = "228FD6"
ClientOrConsumerSecret = getClientSecret()

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
    def __init__(self, config_file = None, user = None):
        self.token_loc_ = config_file
        self.user_ = user
        
    #  Get the config from the config file. This is the access and refresh tokens
    def getTokens(self):
        LOG.info('Calling the database for user: ' + str(self.user_))
        connection = pymysql.connect(host='localhost',
                                     user='user',
                                     db='db')
        try:
            with connection.cursor() as cursor:
                sql = "SELECT access_token, refresh_token from 'tokens' where user = " +\
                      str(self.user_) + "and entered_datetime in " +\
                      "(select max(entered_datetime) from 'tokens' where user = " + self.user_ + ")";
                cursor.execute(sql);
                result = cursor.fetchall()
                access_token, refresh_token = result
            connection.close()
        except:
            #TODO: More useful logging messages, this one is probably important!
            LOG.debug('Failed to retrieve information from database.')
            raise IOError
        
        #TODO: Make result nice.
        return access_token, refresh_token
    #END getTokens()
    
    #  Writes the new tokens to the file.
    def setTokens(self, access_token, refresh_token):
        LOG.info("Writing new tokens to the database")
        LOG.info("Writing this: " + access_token + " and " + refresh_token)
        
        if (access_token==None or refresh_token==None):
            LOG.debug('At least one token passed was none type. Check the rest of the logs for errors.')
            raise IOError
        try:
            connection = pymysql.connect(
                            host='localhost',
                            user='user',
                            b='db')
            with connection.cursor() as cursor:
                sql = "INSERT INTO 'tokens' ('user','access_token','refresh_token') VALUES (%s, %s, %s)"
                cursor.execute(sql, (self.user_, access_token, refresh_token))
                cursor.execute(sql);
                result = cursor.fetchall()
                access_token, refresh_token = result
            connection.close()
            
        except:
            LOG.debug('Failed to write to the database.')
            try:
                LOG.debug('Trying to write to a spare location.')
                file_obj = open(self.token_loc_, 'w')  #NOTE: This deletes old file!
                file_obj.write(access_token + "\n")
                file_obj.write(refresh_token + "\n")
                file_obj.close()
                LOG.debug('Wrote to spare location successfully.')
            except:
                LOG.debug('Problem: FileObj didn\'t properly write the tokens!')
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
        
        #Add the headers, first we base64 encode the client id and client secret with a : inbetween and create the authorisation header
        tokenreq.add_header('Authorization', 'Basic ' + base64.b64encode(OAuthTwoClientID + ":" + ClientOrConsumerSecret))
        tokenreq.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        #Fire off the request
        try:
            token_response = urllib2.urlopen(tokenreq)
            #See what we got back.  If it's this part of  the code it was OK
            full_response = token_response.read()
        
            #Need to pick out the access token and write it to the config file.  Use a JSON manipluation module
            response_json = json.loads(full_response)
        
            #Read the access token as a string
            new_access_token = str(response_json['access_token'])
            new_refresh_token = str(response_json['refresh_token'])
            self.setTokens(new_access_token, new_refresh_token)

            #Return the new tokens to be written or used.
            return new_access_token, new_refresh_token
        
        except urllib2.URLError as e:
            LOG.info("An error was raised when getting the access token.  Need to stop here")
            LOG.info(e.read())
            return None, None
    #END getNewAccessToken()


    ############CLASS VARIABLES##############
    token_loc_ = ''
    token_url_ = "https://api.fitbit.com/oauth2/token"
    user_ = 'None'
    ############CLASS VARIABLES##############

#END TokenGetter class