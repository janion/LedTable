from threading import Thread
from flask import Flask, request

from table.web.flask.FlaskHtmlResponseCreator import HtmlResponseCreator


class WebServerThread(Thread):

    def __init__(self, service):
        Thread.__init__(self, target=service.serverLoop, name="WebServerThread")
        self.setDaemon(True)


class WebServer(object):

    def __init__(self, pixelUpdater, writerFactory, patternManager):
        self.responseCreator = HtmlResponseCreator(pixelUpdater, writerFactory, patternManager)

    def serverLoop(self):
        app = Flask(__name__)
        app.run(host='0.0.0.0', port= 80)

    @app.route('/')
    def homeHandler():
        return self.responseCreator.createResponse(request.path + "?" + request.query_string.decode())

    def stop(self):
        pass
