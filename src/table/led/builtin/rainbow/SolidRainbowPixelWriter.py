from table.led.writer.PixelWriter import PixelWriter2D
from table.led.ColourWheel import ColourWheel
from table.led.configure.custom.CustomConfigurer import CustomConfigurer
from table.led.configure.custom.item.NumberItem import NumberItem
from table.led.configure.custom.item.ColourConverter import ColourConverter


class SolidRainbowPixelWriter(PixelWriter2D):

    NAME = "Solid rainbow fade"

    COLOUR_CONVERTER = ColourConverter()
    DEFAULT_COLOUR_CODE = "#ffffff"

    FADE_SPEED = 10.0
    FADE_SPEED_KEY = "fadeSpeed"
    FADE_SPEED_TITLE = "Fade speed:"

    def __init__(self, ledCountX, ledCountY, mode):
        super(SolidRainbowPixelWriter, self).__init__(ledCountX, ledCountY, mode, self.NAME)
        self.colourWheel = ColourWheel()
        self.colour = None
        self.fadeSpeed = self.FADE_SPEED

        self._createConfiguration()

    def _createConfiguration(self):
        fadeSpeedItem = NumberItem(self.FADE_SPEED_TITLE, self.FADE_SPEED_KEY, self.setFadeSpeed, self.getFadeSpeed)
        self.configurer = CustomConfigurer(self, self.NAME, [fadeSpeedItem])

    def _tick(self, t):
        self.colour = self.colourWheel.getColour(255, t * self.fadeSpeed)

    def _evaluateCell(self, x, y, t):
        return self.colour

    def setFadeSpeed(self, fadeSpeed):
        self.fadeSpeed = float(fadeSpeed)

    def getFadeSpeed(self):
        return self.fadeSpeed
