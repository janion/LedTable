from table.led.ColourWheel import ColourWheel
from table.led.PixelWriter import PixelWriter2D
from table.led.configure.custom.CustomConfigurer import CustomConfigurer
from table.led.configure.custom.item.NumberItem import NumberItem
from table.led.configure.custom.item.ColourConverter import ColourConverter
from table.led.configure.custom.item.ColourItem import ColourItem
from table.led.builtin.automata.wolfram.WolframRules import Rule, DEFAULT_START


class PixelWriter(PixelWriter2D):

    NAME_FORMAT = "Wofram rule %d"
    COLOUR_CONVERTER = ColourConverter()

    STEP_DURATION = 0.25
    DEFAULT_COLOUR = (255, 255, 0)

    FREQUENCY_KEY = "frequency"
    FREQUENCY_TITLE = "Iterations per second:"
    COLOUR_KEY = "colour"
    COLOUR_TITLE = "Cell colour"

    def __init__(self, ledCountX, ledCountY, mode, ruleNumber):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)
        self.name = self.NAME_FORMAT % ruleNumber
        self.colourWheel = ColourWheel()
        self.lastIncrement = None
        self.timeTick = self.STEP_DURATION
        self.rule = Rule(ledCountX, ledCountY, ruleNumber)
        self.rule.setStartCondition(DEFAULT_START)
        self.stepDuration = self.STEP_DURATION
        self.colour = self.DEFAULT_COLOUR

        self._createConfiguration()

    def _createConfiguration(self):
        frequencyItem = NumberItem(self.FREQUENCY_TITLE, self.FREQUENCY_KEY, self.setIterationsPerSecond, self.getIterationsPerSecond)
        colourItem = ColourItem(self.COLOUR_TITLE, self.COLOUR_KEY, self.setColour, self.getColour)

        self.configurer = CustomConfigurer(self, self.name, [frequencyItem, colourItem])

    def _tick(self, t):
        if self.lastIncrement is None:
            self.lastIncrement = t
        if (t - self.lastIncrement) > self.STEP_DURATION:
            self.lastIncrement = t
            self.rule.tick()

    def _evaluateCell(self, x, y, t):
        if self.rule.isPopulated(x, y):
            return self.colour
        else:
            return 0, 0, 0

    def reset(self):
        self.lastIncrement = 0
        self.rule.setStartCondition(DEFAULT_START)

    def setIterationsPerSecond(self, interationsPerSecond):
        self.stepDuration = 1 / float(interationsPerSecond)

    def getIterationsPerSecond(self):
        return int(round(1.0 / self.stepDuration))

    def getColour(self):
        return self.COLOUR_CONVERTER.convertFromColourToHtml(self.colour)

    def setColour(self, colour):
        self.colour = self.COLOUR_CONVERTER.convertFromHtmlToColour(colour)
