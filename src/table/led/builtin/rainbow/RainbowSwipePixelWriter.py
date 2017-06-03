from table.led.PixelWriter import PixelWriter2D
from table.led.ColourWheel import ColourWheel
from math import pow


class PixelWriter(PixelWriter2D):

    DECAY_FACTOR = 0.25
    SECONDS_TO_SWIPE = 1
    MAX_INTENSITY = 255

    def __init__(self, ledCountX, ledCountY, mode):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)
        self.colourWheel = ColourWheel()
        self.angle = 0
        self.lastFrontIndex = 0

    def _tick(self, t):
        frontIndex = self.ledCountX * ((t % self.SECONDS_TO_SWIPE) / self.SECONDS_TO_SWIPE)
        if frontIndex < self.lastFrontIndex:
            self.angle = (self.angle + 60) % 360

    def _evaluateCell(self, x, y, t):
        front = self.ledCountX * ((t % self.SECONDS_TO_SWIPE) / self.SECONDS_TO_SWIPE)
        frontIndex = int(front)
        diffFromFront = ((front - x) + self.ledCountX) % self.ledCountX

        intensity = self.MAX_INTENSITY * pow(self.DECAY_FACTOR, diffFromFront)

        return self.colourWheel.getColour(intensity, self.angle)
