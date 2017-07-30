from table.led.PixelWriter import PixelWriter2D
from table.led.ColourWheel import ColourWheel
from table.led.configure.custom.CustomConfigurer import CustomConfigurer
from table.led.configure.custom.item.NumberItem import NumberItem


class PixelWriter(PixelWriter2D):

    NAME = "Rainbow raster"

    SPEED = 10;
    SPEED_KEY = "speed"
    SPEED_TITLE = "Speed"

    def __init__(self, ledCountX, ledCountY, mode):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)
        self.colourWheel = ColourWheel()
        self.angle = 0
        self.colour = self.colourWheel.getColour(255, 0)
        self.lastTime = 0
        self.speed = self.SPEED
        self.colour = None

        self._createConfiguration()

    def _createConfiguration(self):
        speedItem = NumberItem(self.SPEED_TITLE, self.SPEED_KEY, self.setSpeed, self.getSpeed)
        self.configurer = CustomConfigurer(self, self.NAME, [speedItem])

    def _tick(self, t):
        time = int((t * self.SPEED) % self.ledCount)
        if time == 0 and time < self.lastTime:
            self.angle = (self.angle + 60) % 360
        self.lastTime = time
        self.colour = self.colourWheel.getColour(255, t * 10)

    def _evaluateCell(self, x, y, t):
        if int(((x * self.ledCountY) + y + (t * self.speed)) % self.ledCount) == 0:
            return self.colour
        else:
            return 0, 0, 0

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = float(speed)
