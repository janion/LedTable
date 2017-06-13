from table.led.PixelWriter import PixelWriter2D
from table.led.builtin.text.Text import Text
from table.led.ColourWheel import ColourWheel


class PixelWriter(PixelWriter2D):

    SCROLL_TIME = 0.25
    COLOUR_ANGLE_CHANGE = 12
    BACKGROUND_COLOUR = (0, 0, 0)

    def __init__(self, ledCountX, ledCountY, mode, text):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)
        self.text = Text(ledCountX, ledCountY, text)
        self.lastIncrement = 0
        self.colourWheel = ColourWheel()
        self.colour = self.colourWheel.getColour(255, 0)

    def _tick(self, t):
        self.colour = self.colourWheel.getColour(255, (t - self.startTime) * self.COLOUR_ANGLE_CHANGE)
        if (t - self.lastIncrement) >= self.SCROLL_TIME:
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
