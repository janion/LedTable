import re as regex

from table.web.HtmlFormatter import HtmlFormatter
from table.web.HomePageHtmlCreator import HomePageHtmlCreator
from table.web.UrlParser import UrlParser


class HtmlResponseCreator(object):

    REDIRECT = """<!DOCTYPE html>
    <html>
        <head>
            <script type="text/javascript">
                setTimeout("location.href = '/';",%d);
            </script>
        </head>
        <body>
            %s
        </body>
    </html>
    """

    EMPTY_REDIRECT = REDIRECT % (0, "")

    INVALID_PATTERN_REDIRECT = REDIRECT % (5000, """
            <h1>Invalid pattern functions:</h1><br>
            Red = %s<br>
            Green = %s<br>
            Blue = %s<br>
            You will be redirected in 5 seconds.
    """)

    INVALID_NAME_REDIRECT = REDIRECT % (5000, """
            <h1>Invalid pattern name: %s</h1><br>
            This pattern name is already in use.
            You will be redirected in 5 seconds.
    """)

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
            return self._buildResponse(self.EMPTY_REDIRECT)

        elif path.startswith("/addPattern"):
            name = parameters.get("name", None)
            if self.patterns.isUniqueName(name):
                red = parameters.get("red", None)
                green = parameters.get("green", None)
                blue = parameters.get("blue", None)
                if self.patterns.addPattern(name, red, green, blue):
                    return self._buildResponse(self.EMPTY_REDIRECT)
                else:
                    return self._buildResponse(self.INVALID_PATTERN_REDIRECT %(red, green, blue))
            else:
                return self._buildResponse(self.INVALID_NAME_REDIRECT % name)

        elif path.startswith("/removePattern"):
            name = parameters.get("name", None)
            self.patterns.removePattern(name)
            return self._buildResponse(self.EMPTY_REDIRECT)

        elif path.startswith("/setBrightness"):
            val = int(parameters.get("brightness", 255))
            self.updater.setBrightness(val)
            return self._buildResponse(self.EMPTY_REDIRECT)

        elif path.startswith("/configure"):
            return self._buildResponse(self._configurePattern(parameters))

        return self._buildResponse(self.homePageCreator.buildHomePage(self.patterns))

    def _setPattern(self, name):
        self.patterns.setPattern(name)
        writer = self.patterns.getCurrentWriter()
        self.updater.setPixelWriter(writer)

    def _buildResponse(self, response):
        formattedResponse = HtmlFormatter().formatHtml(response)
        # BUILD HTTP RESPONSE HEADERS
        return '''HTTP/1.0 200 OK\r\nContent-type: text/html\r\nContent-length: %d\r\n\r\n%s''' % (
            len(formattedResponse), formattedResponse)

    def _configurePattern(self, parameters):
        name = parameters.get("name", None)
        config = self.patterns.getWriter(name).getConfigurer()
        return config.configure(parameters)
