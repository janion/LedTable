from table.led.PixelWriter import PixelWriter2D
from table.led.ColourWheel import ColourWheel


class PixelWriter(PixelWriter2D):

    SPEED = 10;

    def __init__(self, ledCountX, ledCountY, mode):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)
        self.colourWheel = ColourWheel()

    def _evaluateCell(self, x, y, t):
        if int(((x * self.ledCountY) + y + (t * self.SPEED)) % self.ledCount) == 0:
            return self.colourWheel.getColour(255, t * 10)
        else:
            return 0, 0, 0
