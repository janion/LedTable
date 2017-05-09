'''
Created on 7 May 2017

@author: Janion
'''

from table.web.WebServer import WebServer, WebServerThread

if __name__ == '__main__':
    WebServerThread(WebServer()).start()
