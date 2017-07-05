import re as regex

from table.web.HomePageHtmlCreator import HomePageHtmlCreator
from table.web.UrlParser import UrlParser


class HtmlResponseCreator(object):

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

    def __init__(self, pixelUpdater, writerFactory, patternManager):
        self.updater = pixelUpdater
        self.writerFactory = writerFactory
        self.patterns = patternManager
        self.urlParser = UrlParser()
        self.homePageCreator = HomePageHtmlCreator()

    def createReponse(self, request):
        # Check is http get request
        obj = regex.search("GET (.*?) HTTP\/1\.1", request)

        if not obj:
            return self._buildResponse("INVALID REQUEST")

        path, parameters = self.urlParser.parseURL(obj.group(1))
        if path.startswith("/setPattern"):
            name = parameters.get("name", None)
            self._setPattern(name)
            return self._buildResponse(self.REDIRECT)
        elif path.startswith("/addPattern"):
            name = parameters.get("name", None)
            red = parameters.get("red", None)
            green = parameters.get("green", None)
            blue = parameters.get("blue", None)
            if self.patterns.addPattern(name, red, green, blue):
                return self._buildResponse(self.REDIRECT)
            else:
                return self._buildResponse(self.INVALID_PATTERN_REDIRECT %(red, green, blue))
        elif path.startswith("/removePattern"):
            name = parameters.get("name", None)
            self.patterns.removePattern(name)
            return self._buildResponse(self.REDIRECT)
        elif path.startswith("/setBrightness"):
            val = int(parameters.get("brightness", 255))
            self.updater.setBrightness(val)
            return self._buildResponse(self.REDIRECT)
        elif path.startswith("/configure"):
            return self._buildResponse(self._configurePattern(parameters))

        return self._buildResponse(self.homePageCreator.buildHomePage(self.patterns))

    def _setPattern(self, name):
        self.patterns.setPattern(name)
        writer = self.patterns.getCurrentWriter()
        self.updater.setPixelWriter(writer)

    def _buildResponse(self, response):
        # BUILD HTTP RESPONSE HEADERS
        return '''HTTP/1.0 200 OK\r\nContent-type: text/html\r\nContent-length: %d\r\n\r\n%s''' % (
            len(response), response)

    def _configurePattern(self, parameters):
        name = parameters.get("name", None)
        config = self.patterns.getWriter(name).getConfigurer()
        return config.configure(parameters)
