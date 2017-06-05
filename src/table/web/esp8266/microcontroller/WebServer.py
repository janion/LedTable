import ure as regex
import socket

from UrlParser import UrlParser
from SerialConnection import SerialConnection


class WebServer(object):

    HTML_FORMAT = """<!DOCTYPE html>
    <html>
        <head>
            <title>Table-top patterns</title>
        </head>
        <body> <h1>Table-top patterns</h1>
            <b>Current pattern:</b> %s<br>
            <form action="/setBrightness">
                <input type="number" name="brightness" min="0" max="255"> <input type="submit" value="Set Brightness (0-255)">
            </form>
            <br>
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

    REDIRECT = """<!DOCTYPE html>
    <html>
        <head>
            <script type="text/javascript">
                window.location.href = "/"
            </script>
        </head>
    </html>
    """

    INVALID_PATTERN_REDIRECT = """<!DOCTYPE html>
    <html>
        <head>
            <script type="text/javascript">
                setTimeout("location.href = '/';",5000);
            </script>
        </head>
        <body>
            <h1>Invalid pattern:</h1><br>
            Red = %s<br>
            Green = %s<br>
            Blue = %s<br>
            You will be redirected in 5 seconds.
        </body>
    </html>
    """

    CUSTOM_PATTERN_ROW_FORMAT = '<tr><td><a href="/setPattern?name=%s">Set</a></td><td>' \
                                '<a href="/removePattern?name=%s">Remove</a></td>' \
                                '<td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'

    BUILTIN_PATTERN_ROW_FORMAT = '<tr><td><a href="/setPattern?name=%s">Set</a></td><td>%s</td></tr>'

    def __init__(self):
        self.serial = SerialConnection()
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
            invalidPattern = False

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
                    if self._addPattern(name, red, green, blue):
                        redirect = True
                    else:
                        invalidPattern = True
                elif path.startswith("/removePattern"):
                    name = parameters.get("name", None)
                    self._removePattern(name)
                    redirect = True
                elif path.startswith("/setBrightness"):
                    val = int(parameters.get("brightness", 255))
                    self._setBrightness(val)
                    redirect = True

            customRows = []
            for p in self.serial.getPatterns():
                customRows.append(self.CUSTOM_PATTERN_ROW_FORMAT % (
                    p.name, p.name, p.name,
                    p.red, p.green, p.blue
                ))
            builtinRows = []
            for name in self.serial.getBuiltinPatternNames():
                builtinRows.append(self.BUILTIN_PATTERN_ROW_FORMAT % (name, name))

            if redirect:
                response = self.REDIRECT
            elif invalidPattern:
                response = self.INVALID_PATTERN_REDIRECT %(red, green, blue)
            else:
                response = self.HTML_FORMAT % (self.serial.getCurrentPatternName(),
                                               '\n'.join(customRows), '\n'.join(builtinRows)
                                               )
            cl.send(response)
        cl.close()

    def _setPattern(self, name):
        self.serial.setPattern(name)

    def _addPattern(self, name, red, green, blue):
        return self.serial.addPattern(name, red, green, blue)

    def _removePattern(self, name):
        self.serial.removePattern(name)

    def _setBrightness(self, val):
        self.serial.setBrightness(val)

    def _buildResponse(self, response):
        # BUILD HTTP RESPONSE HEADERS
        return '''HTTP/1.0 200 OK\r\nContent-type: text/html\r\nContent-length: %d\r\n\r\n%s''' % (
            len(response), response)
