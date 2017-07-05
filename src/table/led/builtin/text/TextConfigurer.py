from table.led.configure.BasicConfigurer import BasicConfigurer


class TextConfigurer(BasicConfigurer):

    HTML_FORMAT = """<!DOCTYPE html>
    <html>
        <head>
            <title>Configure Text</title>
        </head>
        <body> <h1>Configure Text</h1>
            <form action="/configure">
                <b><u>Text to show</u></b><br>
                Text to show:<br>
                <input type="hidden" name="name" value="%s">
                <input type="text" name="text"><br>
                <input type="submit" value="Submit and Set">
            </form>
        </body>
    </html>
    """

    def __init__(self, patternName):
        super(TextConfigurer, self).__init__(patternName)

    def configure(self, parameters):
        text = parameters.get("text")
        if text is not None:
            self.writer.getText().setTextContent(text)
            return self.SET_REDIRECT % self.patternName
        else:
            return self.HTML_FORMAT % self.patternName
