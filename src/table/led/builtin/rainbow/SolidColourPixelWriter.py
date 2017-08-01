from table.led.writer.PixelWriter import PixelWriter2D
from table.led.ColourWheel import ColourWheel
from table.led.configure.custom.CustomConfigurer import CustomConfigurer
from table.led.configure.custom.item.ColourItem import ColourItem
from table.led.configure.custom.item.ColourConverter import ColourConverter


class PixelWriter(PixelWriter2D):

    NAME = "Solid colour"

    COLOUR_CONVERTER = ColourConverter()

    COLOUR = (255, 255, 255)
    COLOUR_KEY = "colour"
    COLOUR_TITLE = "Colour"

    def __init__(self, ledCountX, ledCountY, mode):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, mode, self.NAME)
        self.colourWheel = ColourWheel()
        self.colour = self.COLOUR

        self._createConfiguration()

    def _createConfiguration(self):
        colourItem = ColourItem(self.COLOUR_TITLE, self.COLOUR_KEY, self.setColour, self.getColour)
        self.configurer = CustomConfigurer(self, self.NAME, [colourItem])

    def _tick(self, t):
        self.colour = self.colour

    def _evaluateCell(self, x, y, t):
        return self.colour

    def getColour(self):
        return self.COLOUR_CONVERTER.convertFromColourToHtml(self.colour)

    def setColour(self, colour):
        self.colour = self.COLOUR_CONVERTER.convertFromHtmlToColour(colour)
