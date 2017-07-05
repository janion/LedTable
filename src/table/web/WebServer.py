import socket
from threading import Thread

from table.web.HtmlResponseCreator import HtmlResponseCreator


class WebServerThread(Thread):

    def __init__(self, service):
        Thread.__init__(self, target=service.serverLoop, name="WebServerThread")
        self.setDaemon(True)


class WebServer(object):

    def __init__(self, pixelUpdater, writerFactory, patternManager):
        self.responseCreator = HtmlResponseCreator(pixelUpdater, writerFactory, patternManager)

    def serverLoop(self):
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)

        while True:
            cl, addr = s.accept()
            print('client connected from', addr)
            request = str(cl.recv(1024))
            response = self.responseCreator.createReponse(request)
            cl.send(response)
        cl.close()
