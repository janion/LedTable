'''
Created on 7 May 2017

@author: Janion
'''

from time import sleep
from table.web.WebServer import WebServer, WebServerThread
from table.pattern.PatternManager import PatternManager

if __name__ == '__main__':
    patterns = PatternManager()
    # TODO this doesn't work
    WebServerThread(WebServer(None, None, patterns)).start()

    try:
        while True:
            sleep(0.01)
    except KeyboardInterrupt:
        pass