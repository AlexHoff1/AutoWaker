#https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=228FD6&redirect_uri=https://sites.google.com/a/umn.edu/autowaker/&scope=activity%20nutrition%20heartrate%20location%20nutrition%20profile%20settings%20sleep%20social%20weight
import base64
import urllib2
import urllib
import webbrowser
from fitbit.api import Fitbit

def getAuthCode():
    actual_url = 'https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=228FD6&redirect_uri=https://sites.google.com/a/umn.edu/autowaker/&scope=sleep&expires_in=86400'
    webbrowser.open(actual_url, new = 1)
