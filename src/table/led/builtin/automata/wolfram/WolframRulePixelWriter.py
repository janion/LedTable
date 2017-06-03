from table.led.ColourWheel import ColourWheel
from table.led.PixelWriter import PixelWriter2D
from table.led.builtin.automata.wolfram.WolframRules import Rule, DEFAULT_START


class PixelWriter(PixelWriter2D):

    STEP_DURATION = 0.25

    def __init__(self, ledCountX, ledCountY, mode, ruleNumber):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)
        self.colourWheel = ColourWheel()
        self.lastIncrement = None
        self.timeTick = self.STEP_DURATION
        self.rule = Rule(ledCountX, ledCountY, ruleNumber)
        self.rule.setStartCondition(DEFAULT_START)

    def _tick(self, t):
        if self.lastIncrement is None:
            self.lastIncrement = t
        if (t - self.lastIncrement) > self.STEP_DURATION:
            self.lastIncrement = t
            self.rule.tick()

    def _evaluateCell(self, x, y, t):
        if self.rule.isPopulated(x, y):
            return 255, 255, 0
        else:
            return 0, 0, 0

    def reset(self, t):
        self.lastIncrement = t
        self.rule.setStartCondition(DEFAULT_START)
