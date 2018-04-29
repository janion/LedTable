from threading import Thread
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from table.web.HtmlResponseCreator import HtmlResponseCreator


responseCreator = None


def initResponseCreator( pixelUpdater, writerFactory, patternManager):
    responseCreator = HtmlResponseCreator(pixelUpdater, writerFactory, patternManager)


class WebServerThread(Thread):

    def __init__(self):
        Thread.__init__(self, target=self.run, name="WebServerThread")
        self.setDaemon(True)

    def run(self):
        httpd = HTTPServer(('', 80), Handler)
        httpd.serve_forever()


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.wfile.write(responseCreator.createResponse(self.path))
