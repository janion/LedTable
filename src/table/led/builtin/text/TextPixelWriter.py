from table.led.PixelWriter import PixelWriter2D
from table.led.builtin.text.Text import Text
from table.led.ColourWheel import ColourWheel
from table.led.builtin.text.TextConfigurer import TextConfigurer


class PixelWriter(PixelWriter2D):

    DEFAULT_SCROLL_TIME = 0.25
    COLOUR_ANGLE_CHANGE = 12
    BACKGROUND_COLOUR = (0, 0, 0)

    def __init__(self, ledCountX, ledCountY, mode, text="Hi!"):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode, TextConfigurer("Text"))
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

    def setSecondsPerColumn(self, time):
        self.setSecondsPerColumn(time)
