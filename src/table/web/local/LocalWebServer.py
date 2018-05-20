import socket
from threading import Thread

from table.web.local.LocalHtmlResponseCreator import HtmlResponseCreator


class WebServerThread(Thread):

    def __init__(self, service):
        Thread.__init__(self, target=service.serverLoop, name="WebServerThread")
        self.setDaemon(True)


class WebServer(object):

    def __init__(self, pixelUpdater, writerFactory, patternManager):
        self.responseCreator = HtmlResponseCreator(pixelUpdater, writerFactory, patternManager)

    def serverLoop(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', 83))
        self.sock.listen(1)

        while True:
            cl, addr = self.sock.accept()
            print('client connected from', addr)
            request = cl.recv(1024).decode()
            response = request#self.responseCreator.createResponse(request)
            #response.replace("\n", "")
            # response.replace("\r", "")
            cl.send(response.encode())
            cl.send("\n".encode())
            print("Sent response: " + response)
        cl.close()

    def stop(self):
        self.sock.close()
