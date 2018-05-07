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
        self.sock = socket.socket()
        self.sock.bind(addr)
        self.sock.listen(1)

        while True:
            try:
                cl, addr = self.sock.accept()
                print('client connected from', addr)
                request = str(cl.recv(1024))
                response = self.responseCreator.createResponse(request)
                cl.send(response)
            except ValueError as exptn:
                print(exptn)
                response = self.responseCreator.createResponse("")
                cl.send(response)
        cl.close()

    def stop(self):
        self.sock.close()


# from threading import Thread
# from http.server import BaseHTTPRequestHandler, HTTPServer
# from socketserver import ThreadingMixIn
#
# from table.web.HtmlResponseCreator import HtmlResponseCreator
#
#
# responseCreator = None
# httpd = None
#
#
# def initResponseCreator(pixelUpdater, writerFactory, patternManager):
#     global responseCreator
#     responseCreator = HtmlResponseCreator(pixelUpdater, writerFactory, patternManager)
#
#
# def run():
#     global httpd
#     httpd = ThreadedHttpServer(('', 80), Handler)
#     httpd.timeout = 1
#     httpd.serve_forever()
#
#
# class WebServerThread(Thread):
#
#     def __init__(self):
#         Thread.__init__(self, target=run, name="WebServerThread")
#         self.setDaemon(True)
#
#     def stop(self):
#         global httpd
#         httpd.shutdown()
#
#
# class ThreadedHttpServer(ThreadingMixIn, HTTPServer):
#     """Allows multiple requests to be handled each in a dedicated thread"""
#
#
# class Handler(BaseHTTPRequestHandler):
#
#     def do_GET(self):
#         global responseCreator
#         self.wfile.write(responseCreator.createResponse(self.path).encode())
