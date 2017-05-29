from table.led.builtin.automata.gameoflife.GameOfLife import GameOfLife, R_PENTOMINO

from table.led.ColourWheel import ColourWheel
from table.led.PixelWriter import PixelWriter2D


class PixelWriter(PixelWriter2D):

    STEP_DURATION = 0.25

    def __init__(self, ledCountX, ledCountY, mode):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)
        self.colourWheel = ColourWheel()
        self.startTime = None
        self.lastIncrement = None
        self.timeTick = self.STEP_DURATION
        self.gameOfLife = GameOfLife(ledCountX, ledCountY)
        self.gameOfLife.setStartCondition(R_PENTOMINO)

    def _tick(self, t):
        if self.lastIncrement is None:
            self.lastIncrement = t
        if (t - self.lastIncrement) > self.STEP_DURATION:
            self.lastIncrement = t
            self.gameOfLife.tick()

    def _evaluateCell(self, x, y, t):
        if self.gameOfLife.isPopulated(x, y):
            return 255, 255, 0
        else:
            return 0, 0, 0
