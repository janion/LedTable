from table.led.PixelWriter import PixelWriter2D
from table.led.builtin.text.Text import Text
from table.led.ColourWheel import ColourWheel
from table.led.builtin.text.TextConfigurer import TextConfigurer
from table.led.configure.custom.CustomConfigurer import CustomConfigurer
from table.led.configure.custom.item.TextItem import TextItem
from table.led.configure.custom.item.NumberItem import NumberItem


class PixelWriter(PixelWriter2D):

    NAME = "Text"

    DEFAULT_SCROLL_TIME = 0.25
    COLOUR_ANGLE_CHANGE = 12
    BACKGROUND_COLOUR = (0, 0, 0)
    TEXT_KEY = "text"
    TEXT_TITLE = "Text to show:"
    SPEED_KEY = "speed"
    SPEED_TITLE = "Text speed (Columns per second):"

    def __init__(self, ledCountX, ledCountY, mode, text="Hi!"):
        textItem = TextItem(self.TEXT_TITLE, self.TEXT_KEY, self.setTextContent, self.getTextContent)
        speedItem = NumberItem(self.SPEED_TITLE, self.SPEED_KEY, self.setSecondsPerColumn, self.getSecondsPerColumn)
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode, CustomConfigurer(self.NAME, [textItem, speedItem]))
        self.text = Text(ledCountX, ledCountY, text)
        self.lastIncrement = 0
        self.colourWheel = ColourWheel()
        self.colour = self.colourWheel.getColour(255, 0)
        self.secondsPerColumn = self.DEFAULT_SCROLL_TIME

    def _tick(self, t):
        self.colour = self.colourWheel.getColour(255, (t - self.startTime) * self.COLOUR_ANGLE_CHANGE)
        if (t - self.lastIncrement) >= self.secondsPerColumn:
            self.lastIncrement = t
            self.text.move()

    def reset(self, t):
        super(PixelWriter, self).reset(t)
        self.lastIncrement = t
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

    def setSecondsPerColumn(self, secondsPerColumn):
        self.secondsPerColumn = 1.0 / float(secondsPerColumn)

    def getSecondsPerColumn(self):
        return 1.0 / self.secondsPerColumn
