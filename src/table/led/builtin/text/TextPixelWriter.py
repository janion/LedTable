from table.led.writer.PixelWriter import PixelWriter2D
from table.led.builtin.text.Text import Text
from table.led.ColourWheel import ColourWheel
from table.led.configure.custom.CustomConfigurer import CustomConfigurer
from table.led.configure.custom.item.TextItem import TextItem
from table.led.configure.custom.item.NumberItem import NumberItem
from table.led.configure.custom.item.ColourItem import ColourItem
from table.led.configure.custom.item.CheckboxItem import CheckboxItem
from table.led.configure.custom.item.ColourConverter import ColourConverter


class TextPixelWriter(PixelWriter2D):

    NAME = "Text"

    COLOUR_CONVERTER = ColourConverter()
    DEFAULT_COLOUR_CODE = "#ffffff"

    DEFAULT_TEXT = "Hi!"
    DEFAULT_SCROLL_TIME = 0.25
    COLOUR_ANGLE_CHANGE = 12
    BACKGROUND_COLOUR = (0, 0, 0)
    TEXT_KEY = "text"
    TEXT_TITLE = "Text to show:"
    SPEED_KEY = "speed"
    SPEED_TITLE = "Text speed (Columns per second):"
    COLOUR_KEY = "colour"
    COLOUR_TITLE = "Text colour"
    RAINBOW_COLOUR_KEY = "rainbowColour"
    RAINBOW_COLOUR_TITLE = "Rainbow fade"

    def __init__(self, ledCountX, ledCountY, mode):
        super(TextPixelWriter, self).__init__(ledCountX, ledCountY, mode, self.NAME)
        self._createConfiguration()

        self.text = Text(ledCountX, ledCountY, self.DEFAULT_TEXT)
        self.lastIncrement = 0
        self.colourWheel = ColourWheel()
        self.rainbowColour = True
        self.colour = self.colourWheel.getColour(255, 0)
        self.secondsPerColumn = self.DEFAULT_SCROLL_TIME

    def _createConfiguration(self):
        textItem = TextItem(self.TEXT_TITLE, self.TEXT_KEY, self.setTextContent, self.getTextContent)
        speedItem = NumberItem(self.SPEED_TITLE, self.SPEED_KEY, self.setColumnPerSeconds, self.getColumnPerSeconds)
        colourItem = ColourItem(self.COLOUR_TITLE, self.COLOUR_KEY, self.setColour, self.getColour)
        rainbowColourItem = CheckboxItem(self.RAINBOW_COLOUR_TITLE, self.RAINBOW_COLOUR_KEY, self.setUseRainbowColour,
                                        "TRUE", "configure", self.COLOUR_KEY, False, self.colourIsRainbow)
        self.configurer = CustomConfigurer(self, self.NAME, [textItem, speedItem, colourItem, rainbowColourItem])

    def _tick(self, t):
        if self.rainbowColour:
            self.colour = self.colourWheel.getColour(255, (t - self.startTime) * self.COLOUR_ANGLE_CHANGE)
        if (t - self.lastIncrement) >= self.secondsPerColumn:
            self.lastIncrement = t
            self.text.move()

    def reset(self):
        super(TextPixelWriter, self).reset()
        self.lastIncrement = 0
        self.text.reset()

    def _evaluateCell(self, x, y, t):
        if self.text.isOnChar(x, y):
            return self.colour
        else:
            return self.BACKGROUND_COLOUR

    def setTextContent(self, text):
        self.text.setTextContent(text)

    def getTextContent(self):
        return self.text.getTextContent()

    def setColumnPerSeconds(self, columnPerSeconds):
        self.secondsPerColumn = 1.0 / float(columnPerSeconds)

    def getColumnPerSeconds(self):
        return 1.0 / self.secondsPerColumn

    def setColour(self, colour):
        self.rainbowColour = False
        self.colour = self.COLOUR_CONVERTER.convertFromHtmlToColour(colour)

    def getColour(self):
        if self.colour is not None:
            return self.COLOUR_CONVERTER.convertFromColourToHtml(self.colour)
        else:
            return self.DEFAULT_COLOUR_CODE

    def setUseRainbowColour(self, __):
        self.rainbowColour = True

    def colourIsRainbow(self):
        return self.rainbowColour
