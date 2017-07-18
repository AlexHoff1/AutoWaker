import socket

from AutoWakerHandler import ServerRequestHandler



    
def parseDateAndUser(request):
    information = request.split('\n')
    for line in information:
        lineSplit = line.split(':')
        second = line.strip()
        hardCodedString = 'http://192.168.56.1:8888/?'
        if (second[0:len(hardCodedString)] == hardCodedString):
            params = second[len(hardCodedString):]
            whatWeNeed = params.split('&')
            return whatWeNeed[0], whatWeNeed[1]
    return "", ""        


### TODO: Fix this shitty script and make it real.
HOST, PORT = '192.168.56.1', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...' % PORT
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    print request
    try:
        date, user = parseDateAndUser(request)
    except:
        date, user = "", ""
    print date
    print user
    our_result_maker = ServerRequestHandler(user = user, date = date)
    
    http_response = "HTTP/1.1 200 OK" + "\n" + "\n{\"wakeTime\": \"" + our_result_maker.getWakeTime() + "\"}"

    client_connection.sendall(http_response)
    client_connection.close()
