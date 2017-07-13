from table.led.PixelWriter import PixelWriter2D
from table.led.ColourWheel import ColourWheel
from table.led.configure.custom.CustomConfigurer import CustomConfigurer
from table.led.configure.custom.item.NumberItem import NumberItem
from table.led.configure.custom.validation.ValidationScriptCreator import ValidationScriptCreator
from table.led.configure.custom.item.ColourConverter import ColourConverter
from table.led.configure.custom.item.ColourItem import ColourItem
from table.led.configure.custom.item.CheckboxItem import CheckboxItem
from random import randint


class Cell(object):

    def __init__(self, x, y, t, colour, fadeTime):
        self.x = x
        self.y = y
        self.startTime = t
        self.colour = colour
        self.fadeTime = fadeTime
        self.factor = 1
        self.endTime = self.startTime + self.fadeTime

    def tick(self, t):
        numerator = (t - self.endTime) * (t - self.endTime)
        denominator = self.fadeTime * self.fadeTime
        self.factor = numerator / denominator

    def getColour(self):
        return int(self.colour[0] * self.factor), int(self.colour[1] * self.factor), int(self.colour[2] * self.factor)

    def isExpired(self, t):
        return t >= self.endTime


class PixelWriter(PixelWriter2D):

    NAME = "Stars"

    COLOUR_CONVERTER = ColourConverter()
    DEFAULT_COLOUR_CODE = "#ffffff"

    TIME_BETWEEN_STARS = 0.25
    FADE_TIME = 4.0
    FREQUENCY_KEY = "frequency"
    FREQUENCY_TITLE = "Stars per second:"
    FADE_TIME_KEY = "fadeTime"
    FADE_TIME_TITLE = "Fade time:"
    COLOUR_KEY = "colour"
    COLOUR_TITLE = "Cell colour"
    RANDOM_COLOUR_KEY = "randomColour"
    RANDOM_COLOUR_TITLE = "Use random colour for every cell"

    FIELD_MAP = {"x": FADE_TIME_KEY, "y": FREQUENCY_KEY}
    ERROR_CONDITION = "x * y > %d"
    ERROR_MSG = "Product of fade time and frequency must be less than %d"

    def __init__(self, ledCountX, ledCountY, mode):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)

        self._createConfiguration()

        self.lastIncrement = 0
        self.cells = [[None for y in range(self.ledCountY)] for x in range(self.ledCountX)]
        self.colourWheel = ColourWheel()
        self.timeBetweenStars = self.TIME_BETWEEN_STARS
        self.fadeTime = self.FADE_TIME
        self.colour = None
        self.allowedSpaces = [(x, y) for y in range(self.ledCountY) for x in range(self.ledCountX)]

    def _createConfiguration(self):
        frequencyItem = NumberItem(self.FREQUENCY_TITLE, self.FREQUENCY_KEY, self.setStarsPerSecond, self.getStarsPerSecond)
        fadeTimeItem = NumberItem(self.FADE_TIME_TITLE, self.FADE_TIME_KEY, self.setFadeTime, self.getFadeTime)
        colourItem = ColourItem(self.COLOUR_TITLE, self.COLOUR_KEY, self.setColour, self.getColour)

        randomColourItem = CheckboxItem(self.RANDOM_COLOUR_TITLE, self.RANDOM_COLOUR_KEY, self.setUseRandomColour,
                                        "TRUE", "configure", self.COLOUR_KEY, False, self.colourIsRandom)
        self.configurer = CustomConfigurer(self, self.NAME, [frequencyItem, fadeTimeItem, colourItem, randomColourItem])

        maxVal = self.ledCountX * self.ledCountY
        creator = ValidationScriptCreator(self.ERROR_MSG %maxVal, self.FIELD_MAP, self.ERROR_CONDITION %maxVal)
        self.configurer.setValidation(creator)

    def _tick(self, t):
        for x in range(self.ledCountX):
            for y in range(self.ledCountY):
                if self.cells[x][y] is not None:
                    self.cells[x][y].tick(t)
                    if self.cells[x][y].isExpired(t):
                        self.cells[x][y] = None
                        self.allowedSpaces.append((x, y))

        if (t - self.lastIncrement) >= self.timeBetweenStars:
            if len(self.allowedSpaces) > 0:
                (x, y) = self.allowedSpaces.pop(randint(0, len(self.allowedSpaces) - 1))
                self.cells[x][y] = Cell(x, y, t, self._getColour(), self.fadeTime)
            self.lastIncrement = t

    def _getColour(self):
        if self.colour is None:
            return self.colourWheel.getColour(255, randint(0, 359))
        else:
            return self.colour

    def _evaluateCell(self, x, y, t):
        cell = self.cells[x][y]
        if cell is not None:
            return cell.getColour()
        else:
            return 0, 0, 0

    def reset(self):
        super(PixelWriter, self).reset()
        self.cells = [[None for y in range(self.ledCountY)] for x in range(self.ledCountX)]
        self.allowedSpaces = [(x, y) for y in range(self.ledCountY) for x in range(self.ledCountX)]
        self.lastIncrement = 0

    def setStarsPerSecond(self, starsPerSecond):
        self.timeBetweenStars = 1 / float(starsPerSecond)

    def getStarsPerSecond(self):
        return int(round(1.0 / self.timeBetweenStars))

    def setFadeTime(self, fadeTime):
        self.fadeTime = float(fadeTime)

    def getFadeTime(self):
        return self.fadeTime

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
