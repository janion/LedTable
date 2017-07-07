from table.led.configure.BasicConfigurer import BasicConfigurer


class CustomConfigurer(BasicConfigurer):

    HTML_FORMAT = """<!DOCTYPE html>
    <html>
        <head>
            <title>Configure %s</title>
        </head>
        <body> <h1>Configure %s</h1>
            <form action="/configure">
                <input type="hidden" name="name" value="%s">
                %s
                <input type="submit" value="Submit and Set">
            </form>
        </body>
    </html>
    """

    def __init__(self, patternName, configurationItems):
        super(CustomConfigurer, self).__init__(patternName)
        self.configurationItems = configurationItems

    def setWriter(self, writer):
        self.writer = writer

    def configure(self, parameters):
        setRedirect = False
        for item in self.configurationItems:
            setRedirect = self.configureItem(item, parameters) or setRedirect

        if setRedirect:
            return self.SET_REDIRECT % self.patternName
        else:
            formContent = "\n".join([item.createFormEntry() for item in self.configurationItems])
            return self.HTML_FORMAT % (self.patternName, self.patternName, self.patternName, formContent)

    def configureItem(self, item, parameters):
        value = parameters.get(item.getKey())
        if value is not None:
            item.setValue(value)

        return value is not None
