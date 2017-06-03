from table.led.PixelWriter import PixelWriter2D
from table.led.ColourWheel import ColourWheel


class PixelWriter(PixelWriter2D):

    SPEED = 10;

    def __init__(self, ledCountX, ledCountY, mode):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)
        self.colourWheel = ColourWheel()
        self.angle = 0
        self.colour = self.colourWheel.getColour(255, 0)
        self.lastTime = 0

    def _evaluateCell(self, x, y, t):
        if int(((x * self.ledCountY) + y + (t * self.SPEED)) % self.ledCount) == 0:
            return self.colourWheel.getColour(255, t * 10)
        else:
            return 0, 0, 0

    def _tick(self, t):
        time = int((t * self.SPEED) % self.ledCount)
        if time == 0 and time < self.lastTime:
            self.angle = (self.angle + 60) % 360
        self.lastTime = time
