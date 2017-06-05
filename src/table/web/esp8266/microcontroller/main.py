#from WifiConnector import WifiConnector
from WebServer import WebServer


#WifiConnector().connect()

server = WebServer()
while True:
    try:
        server.serverLoop()
    except Exception:
        pass
