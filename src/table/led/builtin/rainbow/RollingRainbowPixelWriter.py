from table.led.PixelWriter import PixelWriter2D
from table.led.ColourWheel import ColourWheel
from table.led.configure.custom.CustomConfigurer import CustomConfigurer
from table.led.configure.custom.item.NumberItem import NumberItem


class PixelWriter(PixelWriter2D):

    NAME = "Rolling rainbow"

    FADE_SPEED = 10
    COLOUR_PITCH = 20

    FADE_SPEED_KEY = "fadeSpeed"
    FADE_SPEED_TITLE = "Fade speed:"
    COLOUR_PITCH_KEY = "colourPitch"
    COLOUR_PITCH_TITLE = "Colour pitch:"

    def __init__(self, ledCountX, ledCountY, mode):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)
        self.colourWheel = ColourWheel()
        self.fadeSpeed = self.FADE_SPEED
        self.colourPitch = self.COLOUR_PITCH
        self.columnColours = []

        self._createConfiguration()

    def _createConfiguration(self):
        fadeSpeedItem = NumberItem(self.FADE_SPEED_TITLE, self.FADE_SPEED_KEY, self.setFadeSpeed, self.getFadeSpeed)
        colourPitchItem = NumberItem(self.COLOUR_PITCH_TITLE, self.COLOUR_PITCH_KEY, self.setColourPitch, self.getColourPitch)
        self.configurer = CustomConfigurer(self, self.NAME, [fadeSpeedItem, colourPitchItem])

    def _tick(self, t):
        self.columnColours = [self.colourWheel.getColour(255, (t * self.fadeSpeed) + (x * self.colourPitch)) for x in range(self.ledCountX)]

    def _evaluateCell(self, x, y, t):
        return self.columnColours[x]

    def setFadeSpeed(self, fadeSpeed):
        self.fadeSpeed = float(fadeSpeed)

    def getFadeSpeed(self):
        return self.fadeSpeed

    def setColourPitch(self, colourPitch):
        self.colourPitch = float(colourPitch)

    def getColourPitch(self):
        return self.colourPitch
