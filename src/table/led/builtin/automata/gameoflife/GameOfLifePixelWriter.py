from table.led.builtin.automata.gameoflife.GameOfLife import GameOfLife, R_PENTOMINO

from table.led.ColourWheel import ColourWheel
from table.led.PixelWriter import PixelWriter2D
from table.led.configure.custom.CustomConfigurer import CustomConfigurer
from table.led.configure.custom.item.NumberItem import NumberItem
from table.led.configure.custom.item.ColourConverter import ColourConverter
from table.led.configure.custom.item.ColourItem import ColourItem


class PixelWriter(PixelWriter2D):

    NAME = "Game of life"
    COLOUR_CONVERTER = ColourConverter()

    STEP_DURATION = 0.25
    DEFAULT_COLOUR = (255, 255, 0)

    FREQUENCY_KEY = "frequency"
    FREQUENCY_TITLE = "Iterations per second:"
    COLOUR_KEY = "colour"
    COLOUR_TITLE = "Cell colour"

    def __init__(self, ledCountX, ledCountY, mode):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)
        self.colourWheel = ColourWheel()
        self.lastIncrement = None
        self.timeTick = self.STEP_DURATION
        self.gameOfLife = GameOfLife(ledCountX, ledCountY)
        # self.gameOfLife.setStartCondition(R_PENTOMINO)
        self.gameOfLife.setRandomStartCondition()
        self.stepDuration = self.STEP_DURATION
        self.colour = self.DEFAULT_COLOUR

        self._createConfiguration()

    def _createConfiguration(self):
        frequencyItem = NumberItem(self.FREQUENCY_TITLE, self.FREQUENCY_KEY, self.setIterationsPerSecond, self.getIterationsPerSecond)
        colourItem = ColourItem(self.COLOUR_TITLE, self.COLOUR_KEY, self.setColour, self.getColour)

        self.configurer = CustomConfigurer(self, self.NAME, [frequencyItem, colourItem])

    def _tick(self, t):
        if self.lastIncrement is None:
            self.lastIncrement = t
        if (t - self.lastIncrement) > self.stepDuration:
            self.lastIncrement = t
            self.gameOfLife.tick()

    def _evaluateCell(self, x, y, t):
        if self.gameOfLife.isPopulated(x, y):
            return self.colour
        else:
            return 0, 0, 0

    def reset(self):
        self.lastIncrement = 0
        self.gameOfLife.setRandomStartCondition()

    def setIterationsPerSecond(self, interationsPerSecond):
        self.stepDuration = 1 / float(interationsPerSecond)

    def getIterationsPerSecond(self):
        return int(round(1.0 / self.stepDuration))

    def getColour(self):
        return self.COLOUR_CONVERTER.convertFromColourToHtml(self.colour)

    def setColour(self, colour):
        self.colour = self.COLOUR_CONVERTER.convertFromHtmlToColour(colour)
