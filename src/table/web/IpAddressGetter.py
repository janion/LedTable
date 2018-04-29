

def getIpAddress():
    import socket, os
    gw = os.popen("ip -4 route show default").read().split()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if len(gw) >= 3:
        s.connect((gw[2], 0))
        return s.getsockname()[0]
    else:
        return "No Wifi Connection"
