from table.led.configure.BasicConfigurer import BasicConfigurer


class TextConfigurer(BasicConfigurer):

    TEXT_KEY = "text"
    SPEED_KEY = "speed"
    EMPTY = "%s"

    HTML_FORMAT = """<!DOCTYPE html>
    <html>
        <head>
            <title>Configure Text</title>
        </head>
        <body> <h1>Configure Text</h1>
            <form action="/configure">
                <input type="hidden" name="name" value="%s">
                Text to show:<br>
                <input type="text" name="%s" value="%s"><br>
                Text speed (Columns per second):<br>
                <input type="number" name="%s" min="1" max="20" value="%s"><br>
                <input type="submit" value="Submit and Set">
            </form>
        </body>
    </html>
    """ % (EMPTY, TEXT_KEY, EMPTY, SPEED_KEY, EMPTY)

    def __init__(self, patternName):
        super(TextConfigurer, self).__init__(patternName)

    def configure(self, parameters):
        setRedirect = False
        text = parameters.get(self.TEXT_KEY)
        if text is not None:
            self.writer.setTextContent(text)
            setRedirect = True

        speed = parameters.get(self.SPEED_KEY)
        if speed is not None:
            self.writer.setSecondsPerColumn(1 / float(speed))
            setRedirect = True

        if setRedirect:
            return self.SET_REDIRECT % self.patternName
        else:
            textContent = self.writer.getTextContent()
            textSpeed = int(round(1.0 / self.writer.getSecondsPerColumn()))
            return self.HTML_FORMAT % (self.patternName, textContent, textSpeed)
