

def getIpAddress():
    import socket
    return socket.gethostbyname(socket.gethostname())
