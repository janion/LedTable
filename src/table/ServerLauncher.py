'''
Created on 7 May 2017

@author: Janion
'''

from time import sleep
from table.web.WebServer import WebServer, WebServerThread

if __name__ == '__main__':
    WebServerThread(WebServer()).start()

    try:
        while True:
            sleep(0.01)
    except KeyboardInterrupt:
        pass