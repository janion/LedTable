import re as regex
import socket
from threading import Thread

from table.web.UrlParser import UrlParser


class WebServerThread(Thread):

    def __init__(self, service):
        Thread.__init__(self, target=service.serverLoop, name="WebServerThread")
        self.setDaemon(True)


class WebServer(object):

    HTML_FORMAT = """<!DOCTYPE html>
    <html>
        <head>
            <title>Table-top patterns</title>
        </head>
        <body> <h1>Table-top patterns</h1>
            <b>Current pattern:</b> %s<br>
            <table border="1"> <tr><th></th><th></th><th>Name</th><th>Red Function</th><th>Green Function</th><th>Blue Function</th></tr> %s </table>
            <br>
            <table border="1"> <tr><th></th><th>Name</th></tr> %s </table>
            <br>
            <br>
            <form action="/addPattern">
                <b><u>Add Pattern</u></b><br>
                Pattern name:<br>
                <input type="text" name="name"><br>
                Red function:<br>
                <input type="text" name="red"><br>
                Green function:<br>
                <input type="text" name="green"><br>
                Blue function:<br>
                <input type="text" name="blue"><br>
                <br>
                <input type="submit" value="Add pattern">
            </form>
        </body>
    </html>
    """
    REDIRECT = """"<!DOCTYPE html>
    <html>
        <head>
            <script type="text/javascript">
                window.location.href = "/"
            </script>
        </head>
    </html>
    """
    CUSTOM_PATTERN_ROW_FORMAT = '<tr><td><a href="/setPattern?name=%s">Set</a></td><td>' \
                                '<a href="/removePattern?name=%s">Remove</a></td>' \
                                '<td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
    BUILTIN_PATTERN_ROW_FORMAT = '<tr><td><a href="/setPattern?name=%s">Set</a></td><td>%s</td></tr>'

    def __init__(self, pixelUpdater, writerFactory, patternManager):
        self.updater = pixelUpdater
        self.writerFactory = writerFactory
        self.patterns = patternManager
        self.urlParser = UrlParser()

    def serverLoop(self):
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)

        while True:
            cl, addr = s.accept()
            print('client connected from', addr)
            request = str(cl.recv(1024))

            # Check is http get request
            obj = regex.search("GET (.*?) HTTP\/1\.1", request)

            redirect = False

            if not obj:
                cl.send(self._buildResponse("INVALID REQUEST"))
            else:
                path, parameters = self.urlParser.parseURL(obj.group(1))
                if path.startswith("/setPattern"):
                    name = parameters.get("name", None)
                    self._setPattern(name)
                    redirect = True
                elif path.startswith("/addPattern"):
                    name = parameters.get("name", None)
                    red = parameters.get("red", None)
                    green = parameters.get("green", None)
                    blue = parameters.get("blue", None)
                    self.patterns.addPattern(name, red, green, blue)
                    redirect = True
                elif path.startswith("/removePattern"):
                    name = parameters.get("name", None)
                    self.patterns.removePattern(name)
                    redirect = True

            customRows = []
            for p in self.patterns.getPatterns():
                customRows.append(self.CUSTOM_PATTERN_ROW_FORMAT % (
                    p.getName(), p.getName(), p.getName(),
                    p.getRedFunctionString(), p.getGreenFunctionString(),
                    p.getBlueFunctionString()
                ))
            builtinRows = []
            for name in self.patterns.getBuiltinPatternsManager().getPatternNames():
                builtinRows.append(self.BUILTIN_PATTERN_ROW_FORMAT % (name, name))

            if redirect:
                response = self.REDIRECT
            else:
                response = self.HTML_FORMAT % (self.patterns.getCurrentPatternName(),
                                               '\n'.join(customRows), '\n'.join(builtinRows)
                                               )
            cl.send(response)
        cl.close()

    def _setPattern(self, name):
        self.patterns.setPattern(name)
        writer = self.patterns.getWriter()
        self.updater.setPixelWriter(writer)

    def _buildResponse(self, response):
        # BUILD HTTP RESPONSE HEADERS
        return '''HTTP/1.0 200 OK\r\nContent-type: text/html\r\nContent-length: %d\r\n\r\n%s''' % (
            len(response), response)
