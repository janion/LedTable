

class BasicConfigurer(object):

    SET_REDIRECT = """<!DOCTYPE html>
    <html>
        <head>
            <script type="text/javascript">
                window.location.href = "/setPattern?name=%s"
            </script>
        </head>
    </html>
    """

    def __init__(self, patternName):
        self.writer = None
        self.patternName = patternName
        self.isConfigurable = type(self) is not BasicConfigurer

    def setWriter(self, writer):
        self.writer = writer

    def configure(self, parameters):
        return self.SET_REDIRECT % self.patternName
