import socket
import urlparse
import logging
import os

from AutoWakerHandler import ServerRequestHandler
from ConfigHandler import getPath
from TimeHandler import today

HTTP_OK = "HTTP/1.1 200 OK\r\n\r\n"


#  Puts log into a relative location, and adds a day stamp.
def setupServerLogger():
    today_as_dt = today()
    logging.basicConfig(filename='ServerLogs.log',level=logging.INFO, filemode ='w')
    
    # ~/Logs/sleepLogs*date*.log
    relative_log_location = [getPath(), 'Logs', 'ServerLogs' + today_as_dt + '.log']
    hdlr = logging.FileHandler(os.path.join(*relative_log_location))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    
    hdlr.setFormatter(formatter)
    hdlr.setLevel(logging.INFO)
    LOG = logging.getLogger(name = "ServerLogs")
    LOG.addHandler(hdlr)
    LOG.setLevel(logging.INFO)
    return LOG

LOG = setupServerLogger()


# TODO: Clean this up a lot.
def parseDateAndUser(request):
    try:
        information = request.split('\n')
        data = str.split(information[0])
        params = data[1].split('?')[1].split('&') #Get rid of the /?
        for element in params:
            # 0 is the name location, 1 is the data location. Associate name->data.
            parameter_split = element.split('=')
            if parameter_split[0]=='date':
                date = parameter_split[1]
            elif parameter_split[0]=='user':
                user = parameter_split[1]
        return date, user
    except:
        return "","-"

    
#Currently hard coded at port 8888, that will probably conflict with Jupyter. Not sure yet.
def getHostAndPort():
    return socket.getfqdn(), 8888

def assembleHttpResponse(user, date):
    our_result_maker = ServerRequestHandler(user = user, date = date)
    json_information = "{\"wakeTime\": \"" + our_result_maker.getWakeTime() + "\"}"
    return HTTP_OK + json_information

def getListenSocket():
    HOST, PORT = getHostAndPort()
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)
    #While True:
        # make a new socket
        #Return the stuff
        #Start a client thread.
    LOG.info('Serving HTTP on port ' + str(PORT) + ' ...')
    LOG.info("HOST: " + str(HOST) + " and PORT: " + str(PORT))
    return listen_socket

def startServer():
    listen_socket = getListenSocket()

    while True:
        client_connection, client_address = listen_socket.accept()
        request = client_connection.recv(1024)

        print request
        
        date, user = parseDateAndUser(request)
        LOG.info("date is: " + date + " and the user is: " + user)
        
        http_response = assembleHttpResponse(user, date)
    
        client_connection.sendall(http_response)
        client_connection.close()



#SCRIPT TO START A SERVER ON THE MACHINE
startServer()