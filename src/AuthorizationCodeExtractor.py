#https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=228FD6&redirect_uri=https://sites.google.com/a/umn.edu/autowaker/&scope=activity%20nutrition%20heartrate%20location%20nutrition%20profile%20settings%20sleep%20social%20weight
from fitbit.api import Fitbit

def getAuthCode():
    myfitbit = Fitbit(
        client_id='228FD6',
        client_secret='',
        redirect_url='https://sites.google.com/a/umn.edu/autowaker/',
        scope = 'sleep',
        timeout=10)
    url, auth_code = myfitbit.client.authorize_token_url()
    return auth_code
