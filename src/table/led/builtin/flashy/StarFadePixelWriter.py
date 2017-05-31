from table.led.PixelWriter import PixelWriter2D
from table.led.ColourWheel import ColourWheel
from random import randint


class Cell(object):

    FADE_TIME = 4.0

    def __init__(self, x, y, t, colour):
        self.x = x
        self.y = y
        self.startTime = t
        self.colour = colour
        self.factor = 1

    def tick(self, t):
        self.factor = 1 + ((self.startTime - t) / self.FADE_TIME)

    def getColour(self):
        return int(self.colour[0] * self.factor), int(self.colour[1] * self.factor), int(self.colour[2] * self.factor)

    def isExpired(self, t):
        return self.factor <= 0


class PixelWriter(PixelWriter2D):

    TIME_BETWEEN_STARS = 0.25

    def __init__(self, ledCountX, ledCountY, mode):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)
        self.startTime = None
        self.lastIncrement = None
        self.cells = [[None for y in range(self.ledCountY)] for x in range(self.ledCountX)]
        self.colourWheel = ColourWheel()

    def _tick(self, t):
        if self.startTime is None:
            self.startTime = t
            self.lastIncrement = t

        for x in range(self.ledCountX):
            for y in range(self.ledCountY):
                if self.cells[x][y] is not None:
                    self.cells[x][y].tick(t)
                    if self.cells[x][y].isExpired(t):
                        self.cells[x][y] = None

        if (t - self.lastIncrement) >= self.TIME_BETWEEN_STARS:
            x = randint(0, self.ledCountX - 1)
            y = randint(0, self.ledCountY - 1)
            while self.cells[x][y] is not None:
                x = randint(0, self.ledCountX - 1)
                y = randint(0, self.ledCountY - 1)
            self.cells[x][y] = Cell(x, y, t, self.colourWheel.getColour(255, randint(0, 359)))
            self.lastIncrement = t

    def _evaluateCell(self, x, y, t):
        cell = self.cells[x][y]
        if cell is not None:
            return cell.getColour()
        else:
            return 0, 0, 0
