from table.led.PixelWriter import PixelWriter2D
from table.led.ColourWheel import ColourWheel
from table.led.configure.custom.CustomConfigurer import CustomConfigurer
from table.led.configure.custom.item.NumberItem import NumberItem
from table.led.configure.custom.validation.ValidationScriptCreator import ValidationScriptCreator
from table.led.configure.custom.item.ColourConverter import ColourConverter
from table.led.configure.custom.item.ColourItem import ColourItem
from table.led.configure.custom.item.CheckboxItem import CheckboxItem
from table.Constants import LED_COUNT_X,  LED_COUNT_Y
from random import randint
from math import pow


class Swipe(object):

    PROFILE_HEAD_LENGTH = 1
    PROFILE_TAIL_LENGTH = LED_COUNT_X - PROFILE_HEAD_LENGTH

    def __init__(self, y, t, speed, colour):
        self.startY = y
        self.y = y
        self.startTime = t
        self.speed = speed
        self.setColour(colour)

    def setColour(self, colour):
        (self.red, self.green, self.blue) = colour

    def tick(self, t):
        self.y = self.startY - (self.speed * (t - self.startTime))

    def isExpired(self):
        return self.y < -self.PROFILE_TAIL_LENGTH

    def calculate(self):
        cells = {}
        for y in range(1, self.PROFILE_HEAD_LENGTH):
            factor = 1 - (float(y) / self.PROFILE_HEAD_LENGTH)
            cells[int(self.y) - y] = (self.red * factor, self.green * factor, self.blue * factor)

        for y in range(self.PROFILE_TAIL_LENGTH):
            factor = 1 - (float(y) / self.PROFILE_TAIL_LENGTH)
            cells[int(self.y) + y] = (int(self.red * factor), int(self.green * factor), int(self.blue * factor))

        return cells


class PixelWriter(PixelWriter2D):

    NAME = "Swipe"

    COLOUR_CONVERTER = ColourConverter()
    DEFAULT_COLOUR_CODE = "#ffffff"
    
    MAX_INTENSITY = 255

    SWIPE_TIME = 1
    SWIPE_TIME_KEY = "swipeTime"
    SWIPE_TIME_TITLE = "Swipe time:"
    COLOUR_KEY = "colour"
    COLOUR_TITLE = "Colour"
    RANDOM_COLOUR_KEY = "randomColour"
    RANDOM_COLOUR_TITLE = "Use random colour for every swipe"

    def __init__(self, ledCountX, ledCountY, mode):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)
        self.colourWheel = ColourWheel()
        self.lastFront = 10000
        self.colour = None
        self.swipeTime = self.SWIPE_TIME
        self.swipes = []
        self.cells = [[(0, 0, 0) for y in range(self.ledCountY)] for x in range(self.ledCountX)]
        self.lastIncrement = 0

        self._createConfiguration()

    def _createConfiguration(self):
        swipeTimeItem = NumberItem(self.SWIPE_TIME_TITLE, self.SWIPE_TIME_KEY, self.setSwipeTime, self.getSwipeTime, step=0.1)
        colourItem = ColourItem(self.COLOUR_TITLE, self.COLOUR_KEY, self.setColour, self.getColour)

        randomColourItem = CheckboxItem(self.RANDOM_COLOUR_TITLE, self.RANDOM_COLOUR_KEY, self.setUseRandomColour,
                                        "TRUE", "configure", self.COLOUR_KEY, False, self.colourIsRandom)
        self.configurer = CustomConfigurer(self, self.NAME, [swipeTimeItem, colourItem, randomColourItem])

    def _tick(self, t):
        self.cells = [[(0, 0, 0) for y in range(self.ledCountY)] for x in range(self.ledCountX)]
        for i in range(len(self.swipes)):
            swipe = self.swipes[i]
            swipe.tick(t)
            if swipe.isExpired():
                self.swipes[i] = None
            else:
                for (y, brightness) in swipe.calculate().iteritems():
                    if 0 <= y < LED_COUNT_Y:
                        for x in range(LED_COUNT_X):
                            self.cells[x][y] = brightness

        for __ in range(self.swipes.count(None)):
            self.swipes.remove(None)

        if (t - self.lastIncrement) >= self.swipeTime:
            if self.colour is None:
                colour = self.colourWheel.getColour(self.MAX_INTENSITY, randint(0, 359))
            else:
                colour = self.colour
            swipe = Swipe(LED_COUNT_Y, t, LED_COUNT_X / self.swipeTime, colour)
            self.swipes.append(swipe)
            self.lastIncrement = t

    def _evaluateCell(self, x, y, t):
        colour = self.cells[x][self.ledCountY - (y + 1)]
        return colour

    def reset(self):
        super(PixelWriter, self).reset()
        self.lastIncrement = 0
        self.swipes = []

    def setSwipeTime(self, swipeTime):
        self.swipeTime = float(swipeTime)

    def getSwipeTime(self):
        return float(self.swipeTime)

    def getColour(self):
        if self.colour is not None:
            return self.COLOUR_CONVERTER.convertFromColourToHtml(self.colour)
        else:
            return self.DEFAULT_COLOUR_CODE

    def setColour(self, colour):
        self.colour = self.COLOUR_CONVERTER.convertFromHtmlToColour(colour)

    def setUseRandomColour(self, __):
        self.colour = None

    def colourIsRandom(self):
        return self.colour is None
