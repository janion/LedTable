from table.led.PixelWriter import PixelWriter2D
from table.led.ColourWheel import ColourWheel
from table.led.configure.custom.CustomConfigurer import CustomConfigurer
from table.led.configure.custom.item.ColourItem import ColourItem
from table.led.configure.custom.item.NumberItem import NumberItem
from table.led.configure.custom.item.ColourConverter import ColourConverter


class PixelWriter(PixelWriter2D):

    NAME = "Raster"

    COLOUR_CONVERTER = ColourConverter()

    COLOUR = (255, 255, 255)
    COLOUR_KEY = "colour"
    COLOUR_TITLE = "Colour"

    SPEED = 10;
    SPEED_KEY = "speed"
    SPEED_TITLE = "Speed"

    def __init__(self, ledCountX, ledCountY, mode):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)
        self.colourWheel = ColourWheel()
        self.colour = self.COLOUR
        self.speed = self.SPEED

        self._createConfiguration()

    def _createConfiguration(self):
        colourItem = ColourItem(self.COLOUR_TITLE, self.COLOUR_KEY, self.setColour, self.getColour)
        speedItem = NumberItem(self.SPEED_TITLE, self.SPEED_KEY, self.setSpeed, self.getSpeed)
        self.configurer = CustomConfigurer(self, self.NAME, [colourItem, speedItem])

    def _evaluateCell(self, x, y, t):
        if int(((x * self.ledCountY) + y + (t * self.speed)) % self.ledCount) == 0:
            return self.colour
        else:
            return 0, 0, 0

    def getColour(self):
        return self.COLOUR_CONVERTER.convertFromColourToHtml(self.colour)

    def setColour(self, colour):
        self.colour = self.COLOUR_CONVERTER.convertFromHtmlToColour(colour)

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = float(speed)
