from table.led.configure.BasicConfigurer import BasicConfigurer


class CustomConfigurer(BasicConfigurer):

    HTML_FORMAT = """<!DOCTYPE html>
    <html>
        <head>
            <title>Configure %s</title>
            %s
        </head>
        <body> <h1>Configure %s</h1>
            <form name="configure" action="/configure"%s>
                <input type="hidden" name="name" value="%s">
                %s
                <input type="submit" name="action" value="Submit">
                <input type="submit" name="action" value="Submit and Set">
            </form>
        </body>
    </html>
    """

    SET_REDIRECT = """<!DOCTYPE html>
    <html>
        <head>
            <script type="text/javascript">
                window.location.href = "/setPattern?name=%s"
            </script>
        </head>
    </html>
    """

    EMPTY = ""

    def __init__(self, writer, patternName, configurationItems):
        super(CustomConfigurer, self).__init__()
        self.patternName = patternName
        self.configurationItems = configurationItems
        self.writer = writer
        self.validationScript = self.EMPTY
        self.validationAction = self.EMPTY

    def setValidation(self, validationCreator):
        self.validationScript = validationCreator.createValidationScript()
        self.validationAction = validationCreator.createValidatingFormAction()

    def configure(self, parameters):
        for item in self.configurationItems:
            self.configureItem(item, parameters)

        action = parameters.get("action")
        if action is not None:
            if action == "Submit and Set":
                return self.SET_REDIRECT % self.patternName
            else:
                return self.REDIRECT
        else:
            formContent = "\n".join([item.createFormEntry() for item in self.configurationItems])
            return self.HTML_FORMAT % (self.patternName, self.validationScript, self.patternName,
                                       self.validationAction, self.patternName, formContent)

    def configureItem(self, item, parameters):
        value = parameters.get(item.getKey())
        if value is not None:
            item.setValue(value)
