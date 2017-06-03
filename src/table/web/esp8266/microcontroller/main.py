from table.web.esp8266.microcontroller.WifiConnector import WifiConnector
from table.web.esp8266.microcontroller.WebServer import WebServer


WifiConnector().connect()

server = WebServer()
while True:
    try:
        server.serverLoop()
    except Exception:
        pass
