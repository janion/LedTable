from table.led.writer.PixelWriter import PixelWriter2D
from table.led.ColourWheel import ColourWheel
from table.led.configure.custom.CustomConfigurer import CustomConfigurer
from table.led.configure.custom.item.NumberItem import NumberItem


class RollingRainbowPixelWriter(PixelWriter2D):

    NAME = "Rolling rainbow"

    FADE_SPEED = 10
    COLOUR_PITCH = 20

    FADE_SPEED_KEY = "speed"
    FADE_SPEED_TITLE = "Speed:"
    COLOUR_PITCH_KEY = "colourPitch"
    COLOUR_PITCH_TITLE = "Colour pitch:"

    def __init__(self, ledCountX, ledCountY, mode):
        super(RollingRainbowPixelWriter, self).__init__(ledCountX, ledCountY, mode, self.NAME)
        self.colourWheel = ColourWheel()
        self.speed = self.FADE_SPEED
        self.colourPitch = self.COLOUR_PITCH
        self.columnColours = []

        self._createConfiguration()

    def _createConfiguration(self):
        speedItem = NumberItem(self.FADE_SPEED_TITLE, self.FADE_SPEED_KEY, self.setSpeed, self.getSpeed)
        colourPitchItem = NumberItem(self.COLOUR_PITCH_TITLE, self.COLOUR_PITCH_KEY, self.setColourPitch, self.getColourPitch)
        self.configurer = CustomConfigurer(self, self.NAME, [speedItem, colourPitchItem])

    def _tick(self, t):
        self.columnColours = [self.colourWheel.getColour(255, (t * self.speed) + (x * self.colourPitch)) for x in range(self.ledCountX)]

    def _evaluateCell(self, x, y, t):
        return self.columnColours[x]

    def setSpeed(self, speed):
        self.speed = float(speed)

    def getSpeed(self):
        return self.speed

    def setColourPitch(self, colourPitch):
        self.colourPitch = float(colourPitch)

    def getColourPitch(self):
        return self.colourPitch
