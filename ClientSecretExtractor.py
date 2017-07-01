def getClientSecret():
    fid = open('/Users/Owner/Desktop/Code/AutoWaker/Data/ClientSecret.txt')
    client_secret = fid.read()
    fid.close()
    return client_secret.strip()