from table.led.PixelWriter import PixelWriter2D
from table.led.ColourWheel import ColourWheel


class PixelWriter(PixelWriter2D):

    DECAY_FACTOR = 0.25
    SECONDS_TO_SWIPE = 1
    MAX_INTENSITY = 255

    def __init__(self, ledCountX, ledCountY, mode):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)
        self.colourWheel = ColourWheel()

    def _evaluateCell(self, x, y, t):
        return self.colourWheel.getColour(255, t * 10)
