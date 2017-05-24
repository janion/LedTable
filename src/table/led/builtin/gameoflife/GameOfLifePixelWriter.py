from table.led.PixelWriter import PixelWriter2D
from table.led.ColourWheel import ColourWheel
from table.led.builtin.gameoflife.GameOfLife import GameOfLife


class PixelWriter(PixelWriter2D):

    STEP_DURATION = 0.25

    def __init__(self, ledCountX, ledCountY, mode):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)
        self.colourWheel = ColourWheel()
        self.startTime = None
        self.lastIncrement = None
        self.timeTick = self.STEP_DURATION
        self.gameOfLife = GameOfLife(ledCountX, ledCountY)
        # self.gameOfLife.setStartCondition([(4, 0), (4, 1), (4, 2), (4, 3), (4, 4),
        #                                    (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
        #
        #                                    (0, 4), (1, 4), (2, 4), (3, 4), (5, 4),
        #                                    (6, 4), (7, 4), (8, 4), (9, 4),
        #
        #                                    (0, 7), (1, 7), (2, 7), (3, 7), (5, 7),
        #                                    (6, 7), (7, 7), (8, 7), (9, 7),
        #
        #                                    (7, 0), (7, 1), (7, 2), (7, 3),
        #                                    (8, 5), (8, 6), (8, 8), (8, 9),
        #
        #                                    (1, 0), (1, 1), (2, 2), (3, 3), (4, 4),
        #                                    (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)
        #                                    ])
        self.gameOfLife.setStartCondition([(1, 0), (1, 1), (2, 2), (3, 3), (4, 4),
                                           (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (8, 9)
                                           ])

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
