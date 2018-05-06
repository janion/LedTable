import re


class HtmlFormatter(object):

    TAG_REGEX = "(.*?)<(.*?)>"
    END_TAG_FORMAT = "</%s>"
    TAB = "    "
    SLASH = "/"
    COMMENT = "!"
    SPACE = " "
    OPEN_BRACKET = "{"
    CLOSE_BRACKET = "}"

    def formatHtml(self, htmlString):
        lines = htmlString.split("\n")
        for i in range(len(lines)):
            lines[i] = lines[i].strip()

        self._indentTags(lines, htmlString)
        self._indentStyle(lines)

        return "\n".join(lines)

    def _indentTags(self, lines, htmlString):
        for lineCount in range(len(lines)):
            line = lines[lineCount]
            match = re.match(self.TAG_REGEX, line)
            if match:
                tag = match.group(2).split(self.SPACE)[0]
                endTag = self.END_TAG_FORMAT %tag
                if tag.startswith(self.SLASH) or tag.startswith(self.COMMENT) or endTag not in htmlString:
                    continue
                if endTag not in line:
                    for nextLineCount in range(lineCount + 1, len(lines)):
                        nextLine = lines[nextLineCount]
                        if endTag not in nextLine:
                            lines[nextLineCount] = self.TAB + nextLine
                        else:
                            break

    def _indentStyle(self, lines):
        for lineCount in range(len(lines)):
            line = lines[lineCount]
            if self.OPEN_BRACKET in line:
                if self.CLOSE_BRACKET not in line:
                    for nextLineCount in range(lineCount + 1, len(lines)):
                        nextLine = lines[nextLineCount]
                        if self.CLOSE_BRACKET not in nextLine:
                            lines[nextLineCount] = self.TAB + nextLine
                        else:
                            break

if __name__ == "__main__":
    raw = """
<html>
    <body>
        <form>
        hi, what?
        <td>hh</td>
</form>
</body>
</html>
    """

    formatted = HtmlFormatter().formatHtml(raw)
    print(raw)
    print()
    print(formatted)

    raw = """
<!DOCTYPE html>
    <html>
        <head>
            <title>Table-top patterns</title>
<style>
table {
    border-collapse: collapse;
    width: 100%;
    white-space: nowrap;
}

th, td {
    padding: 2px;
    text-align: center;
    border-bottom: 1px solid #ddd;
}
th {
    background-color: #5050FF;
    color: white;
}

tr:hover{background-color:#f5f5f5}
</style>
        </head>
        <body>
        <h1>Table-top patterns</h1>
            <b>Current pattern:</b> Stars<br>
            <form action="/setBrightness">
                <input type="number" name="brightness" min="0" max="255"> <input type="submit" value="Set Brightness (0-255)">
            </form>
            <br>
<div style="overflow-x:auto;">
            <table border="1">
            <tr><th></th><th></th><th>Name</th><th>Red Function</th><th>Green Function</th><th>Blue Function</th></tr> <tr><td><a href="/setPattern?name=one">Set</a></td><td><a href="/removePattern?name=one">Remove</a></td><td>one</td><td>x</td><td>x</td><td>x</td></tr>
<tr><td><a href="/setPattern?name=two">Set</a></td><td><a href="/removePattern?name=two">Remove</a></td><td>two</td><td>sin(x)</td><td>sin(y)</td><td>cos(t)</td></tr>
<tr><td><a href="/setPattern?name=three">Set</a></td><td><a href="/removePattern?name=three">Remove</a></td><td>three</td><td>3 * x</td><td>3 * x</td><td>3 * x</td></tr>
</table>
</div>
            <br>
            <div style="overflow-x:auto;">
            <table border="1">
            <tr><th></th><th>Name</th><th></th></tr> <tr><td><a href="/setPattern?name=Rainbow swipe">Set</a></td><td>Rainbow swipe</td><td></td></tr>
<tr><td><a href="/setPattern?name=Dot raster">Set</a></td><td>Dot raster</td><td></td></tr>
<tr><td><a href="/setPattern?name=Dot raster fade">Set</a></td><td>Dot raster fade</td><td></td></tr>
<tr><td><a href="/setPattern?name=Stars">Set</a></td><td>Stars</td><td><a href="/configure?name=Stars">Configure</a></td></tr>
<tr><td><a href="/setPattern?name=Text">Set</a></td><td>Text</td><td><a href="/configure?name=Text">Configure</a></td></tr>
<tr><td><a href="/setPattern?name=Solid rainbow fade">Set</a></td><td>Solid rainbow fade</td><td></td></tr>
<tr><td><a href="/setPattern?name=Game of life">Set</a></td><td>Game of life</td><td></td></tr>
<tr><td><a href="/setPattern?name=Rule 30">Set</a></td><td>Rule 30</td><td></td></tr>
<tr><td><a href="/setPattern?name=Snake">Set</a></td><td>Snake</td><td></td></tr>
<tr><td><a href="/setPattern?name=Rainbow roll">Set</a></td><td>Rainbow roll</td><td></td></tr>
</table>
</div>
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
    </html>"""

    formatted = HtmlFormatter().formatHtml(raw)
    print(raw)
    print()
    print(formatted)
