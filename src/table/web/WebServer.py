from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

from table.web.HtmlResponseCreator import HtmlResponseCreator


responseCreator = None
httpd = None


def initResponseCreator(pixelUpdater, writerFactory, patternManager):
    global responseCreator
    responseCreator = HtmlResponseCreator(pixelUpdater, writerFactory, patternManager)


def run():
    global httpd
    httpd = ThreadedHttpServer(('', 80), Handler)
    httpd.serve_forever()


class WebServerThread(Thread):

    def __init__(self):
        Thread.__init__(self, target=run, name="WebServerThread")
        self.setDaemon(True)

    def stop(self):
        global httpd
        httpd.shutdown()
        super(WebServerThread, self).stop()


class ThreadedHttpServer(ThreadingMixIn, HTTPServer):
    """Allows multiple requests to be handled each in a dedicated thread"""


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        global responseCreator
        self.wfile.write(responseCreator.createResponse(self.path))
