'''
Created on 6 May 2017

@author: Janion
'''


class PixelWriter1D(object):

    def __init__(self, ledCount, pattern):
        self.data = [(0, 0, 0) for x in range(ledCount)]
        self.ledCount = ledCount
        if pattern is not None:
            self.rFunc = pattern.getRedFunction()
            self.gFunc = pattern.getGreenFunction()
            self.bFunc = pattern.getBlueFunction()

    def getPixelData(self, t):
        for x in range(self.ledCount):
            self.data[x] = (int(self.rFunc.evaluate(x, 0, t)[0]),
                            int(self.gFunc.evaluate(x, 0, t)[0]),
                            int(self.bFunc.evaluate(x, 0, t)[0])
                            )
        return self.data


class PixelWriter2D(PixelWriter1D):

    RASTER = 0
    ZIG_ZAG = 1

    def __init__(self, ledCountX, ledCountY, pattern, mode):
        super(PixelWriter2D, self).__init__(ledCountX * ledCountY, pattern)
        self.ledCountX = ledCountX
        self.ledCountY = ledCountY
        self.mode = mode

    def getPixelData(self, t):
        if self.mode == self.RASTER:
            for x in range(self.ledCountX):
                self._makeColumnForwards(x, t)
        elif self.mode == self.ZIG_ZAG:
            for x in range(self.ledCountX):
                if (x % 2) == 0:
                    self._makeColumnForwards(x, t)
                else:
                    self._makeColumnBackwards(x, t)

        return self.data

    def _makeColumnForwards(self, x, t):
        for y in range(self.ledCountY):
            index = (x * self.ledCountY) + y
            self.data[index] = self._evaluateCell(x, y, t)

    def _makeColumnBackwards(self, x, t):
        for y in range(self.ledCountY - 1, -1, -1):
            index = (x * self.ledCountY) + (self.ledCountY - (y + 1))
            self.data[index] = self._evaluateCell(x, y, t)

    def _evaluateCell(self, x, y, t):
        return (int(self.rFunc.evaluate(x, y, t)[0]),
                int(self.gFunc.evaluate(x, y, t)[0]),
                int(self.bFunc.evaluate(x, y, t)[0])
                )
