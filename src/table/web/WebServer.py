from threading import Thread
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from table.web.HtmlResponseCreator import HtmlResponseCreator


responseCreator = None
httpd = None


def initResponseCreator( pixelUpdater, writerFactory, patternManager):
    global responseCreator
    responseCreator = HtmlResponseCreator(pixelUpdater, writerFactory, patternManager)


def run(self):
    global httpd
    httpd = HTTPServer(('', 80), Handler)
    httpd.serve_forever()


class WebServerThread(Thread):

    def __init__(self):
        Thread.__init__(self, target=run, name="WebServerThread")
        self.setDaemon(True)

    def stop(self):
        global httpd
        httpd.shutdown()
        super().stop()
        # super(WebServerThread, self).stop()


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.wfile.write(responseCreator.createResponse(self.path))
