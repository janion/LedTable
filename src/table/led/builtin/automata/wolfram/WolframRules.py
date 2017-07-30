from table.Constants import LED_COUNT_X
from random import randint


DEFAULT_START = [(LED_COUNT_X / 2) - 1]


class Rule(object):

    def __init__(self, gridSizeX, gridSizeY, ruleNumber, randomBoundaries = True):
        self.gridSizeX = gridSizeX
        self.gridSizeY = gridSizeY
        self.ruleNumber = ruleNumber
        self.randomBoundaries = randomBoundaries
        self.data = [[0 for y in range(self.gridSizeY)] for x in range(self.gridSizeX)]

    def setStartCondition(self, positions):
        self.data = [[0 for y in range(self.gridSizeY)] for x in range(self.gridSizeX)]
        for pos in positions:
            self.data[pos][self.gridSizeY - 1] = 1

    def isPopulated(self, x, y):
        return self.data[x][y] == 1

    def tick(self):
        for x in range(self.gridSizeX):
            for y in range(self.gridSizeY - 1):
                self.data[x][y] = self.data[x][y + 1]

        nextTick = self._calculateNextTick()
        for x in range(len(nextTick)):
            self.data[x][self.gridSizeY - 1] = nextTick[x]

    def _calculateNextTick(self):
        nextTick = [0 for x in range(self.gridSizeX)]
        if self.randomBoundaries:
            lastTick = [randint(0, 1)] + [self.data[x][self.gridSizeY - 2] for x in xrange(self.gridSizeX)] + [randint(0, 1)]
        else:
            lastTick = [0] + [self.data[x][self.gridSizeY - 2] for x in xrange(self.gridSizeX)] + [0]
        for x in range(self.gridSizeX):
            aboveVal = self._getAboveValue(lastTick, x + 1)
            if 1 & (self.ruleNumber >> aboveVal) == 1:
                nextTick[x] = 1

        return nextTick

    def _getAboveValue(self, lastTick, index):
        val = 0
        for x in range(-1, 2):
            val += lastTick[index + x] << (1 - x)
        return val
