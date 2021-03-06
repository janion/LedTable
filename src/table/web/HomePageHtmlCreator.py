from table.web.HeadCreator import HeadCreator


class HomePageHtmlCreator(object):

    HTML_FORMAT = """<!DOCTYPE html>
    <html>
        %s
        <body>
            <h1>Table-top patterns</h1>
            <b>Current pattern:</b> %s<br>
            <form action="/setBrightness">
                <input type="number" name="brightness" min="0" max="255"> <input type="submit" value="Set Brightness (0-255)">
            </form>
            <br>
            <div style="overflow-x:auto;">
                <table border="1">
                    <tr><th></th><th>Name</th><th></th></tr> %s
                </table>
            </div>
            <br>
            <div style="overflow-x:auto;">
                <table border="1">
                    <tr><th></th><th></th><th>Name</th><th>Red Function</th><th>Green Function</th><th>Blue Function</th></tr> %s
                </table>
            </div>
            <br>
            <br>
            <form name="addPattern" action="/addPattern" onsubmit="return validateName()">
                <b><u>Add Pattern</u></b><br>
                Pattern name:<br>
                <input type="text" name="name" required><br>
                Red function:<br>
                <input type="text" name="red" required><br>
                Green function:<br>
                <input type="text" name="green" required><br>
                Blue function:<br>
                <input type="text" name="blue" required><br>
                <br>
                <input type="submit" value="Add pattern">
            </form>
        </body>
    </html>
    """

    CUSTOM_PATTERN_ROW_FORMAT = '<tr><td><a href="/setPattern?name=%s">Set</a></td><td>' \
                                '<a href="/removePattern?name=%s">Remove</a></td>' \
                                '<td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'

    BUILTIN_PATTERN_ROW_FORMAT = '<tr><td><a href="/setPattern?name=%s">Set</a></td><td>%s</td><td>%s</td></tr>'

    LINK_FORMAT = '<a href="/configure?name=%s">Configure</a>'


    def buildHomePage(self, patternManager):
        customRows = self._buildCustomPatternHtmlTable(patternManager)
        builtinRows = self._buildBuiltinPatternHtmlTable(patternManager)
        response = self.HTML_FORMAT % (HeadCreator().createHead(patternManager), patternManager.getCurrentPatternName(),
                                       '\n'.join(builtinRows), '\n'.join(customRows)
                                       )
        return response

    def _buildCustomPatternHtmlTable(self, patternManager):
        customRows = []
        for p in patternManager.getPatterns():
            customRows.append(self.CUSTOM_PATTERN_ROW_FORMAT % (
                p.getName(), p.getName(), p.getName(),
                p.getRedFunctionString(), p.getGreenFunctionString(),
                p.getBlueFunctionString()
            ))
        return customRows

    def _buildBuiltinPatternHtmlTable(self, patternManager):
        builtinRows = []
        builtinManager = patternManager.getBuiltinPatternsManager()
        for name in builtinManager.getPatternNames():
            configurer = builtinManager.getWriter(name).getConfigurer()
            finalColumn = self.LINK_FORMAT % name if configurer.isConfigurable else ""
            builtinRows.append(self.BUILTIN_PATTERN_ROW_FORMAT % (name, name, finalColumn))
        return builtinRows
