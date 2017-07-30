from table.led.PixelWriter import PixelWriter2D
from table.led.ColourWheel import ColourWheel
from table.led.configure.custom.CustomConfigurer import CustomConfigurer
from table.led.configure.custom.item.NumberItem import NumberItem
from table.led.configure.custom.validation.ValidationScriptCreator import ValidationScriptCreator
from table.led.configure.custom.item.ColourConverter import ColourConverter
from table.led.configure.custom.item.ColourItem import ColourItem
from table.led.configure.custom.item.CheckboxItem import CheckboxItem
from random import randint
from math import pow


class PixelWriter(PixelWriter2D):

    NAME = "Swipe"

    COLOUR_CONVERTER = ColourConverter()
    DEFAULT_COLOUR_CODE = "#e0e0ff"

    DECAY_FACTOR = 0.25
    SECONDS_TO_SWIPE = 1
    MAX_INTENSITY = 255

    def __init__(self, ledCountX, ledCountY, mode):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)
        self.colourWheel = ColourWheel()
        self.angle = 0
        self.lastFront = 10000
        self.randomColour = True
        self.colour = self.colourWheel.getColour(self.MAX_INTENSITY, randint(0, 359))

    def _tick(self, t):
        front = self.ledCountX * ((t % self.SECONDS_TO_SWIPE) / self.SECONDS_TO_SWIPE)
        if front < self.lastFront and self.randomColour:
            self.colour = self.colourWheel.getColour(self.MAX_INTENSITY, randint(0, 359))

    def _evaluateCell(self, x, y, t):
        front = self.ledCountX * ((t % self.SECONDS_TO_SWIPE) / self.SECONDS_TO_SWIPE)
        self.lastFront = front
        diffFromFront = ((front - x) + self.ledCountX) % self.ledCountX

        intensity = self.MAX_INTENSITY * pow(self.DECAY_FACTOR, diffFromFront)

        if intensity > 255 or intensity < 0:
            print intensity

        return (intensity * self.colour[0], intensity * self.colour[1], intensity * self.colour[2])

    def getColour(self):
        if self.colour is not None:
            return self.COLOUR_CONVERTER.convertFromColourToHtml(self.colour)
        else:
            return self.DEFAULT_COLOUR_CODE

    def setColour(self, colour):
        self.colour = self.COLOUR_CONVERTER.convertFromHtmlToColour(colour)
        self.randomColour = False

    def setUseRandomColour(self, __):
        self.randomColour = True

    def colourIsRandom(self):
        return self.randomColour
