'''
Created on 6 May 2017

@author: Janion
'''

from table.led.configure.BasicConfigurer import BasicConfigurer


class PixelWriter1D(object):

    def __init__(self, ledCount, name):
        self.ledCount = ledCount
        self.name = name
        self.startTime = 0
        self.configurer = BasicConfigurer()

    def getName(self):
        return self.name

    def getPixelData(self, t):
        self._tick(t)
        return self._calculate(t)

    def _tick(self, t):
        pass

    def _calculate(self, t):
        return [(0, 0, 0) for __ in range(self.ledCount)]

    def reset(self):
        self.startTime = 0

    def getConfigurer(self):
        return self.configurer


class PixelWriter2D(PixelWriter1D):

    RASTER = "RASTER"
    ZIG_ZAG = "ZIG_ZAG"

    def __init__(self, ledCountX, ledCountY, mode, name):
        super(PixelWriter2D, self).__init__(ledCountX * ledCountY, name)
        self.ledCountX = ledCountX
        self.ledCountY = ledCountY
        self.mode = mode

    def _calculate(self, t):
        data = super(PixelWriter2D, self)._calculate(t)
        if self.mode == self.RASTER:
            for x in range(self.ledCountX):
                self._makeColumnForwards(x, t, data)
        elif self.mode == self.ZIG_ZAG:
            for x in range(self.ledCountX):
                if (x % 2) == 0:
                    self._makeColumnForwards(x, t, data)
                else:
                    self._makeColumnBackwards(x, t, data)
        return data

    def _makeColumnForwards(self, x, t, data):
        for y in range(self.ledCountY):
            index = (x * self.ledCountY) + y
            data[index] = self._evaluateCell(x, y, t)

    def _makeColumnBackwards(self, x, t, data):
        for y in range(self.ledCountY - 1, -1, -1):
            index = (x * self.ledCountY) + (self.ledCountY - (y + 1))
            data[index] = self._evaluateCell(x, y, t)

    def _evaluateCell(self, x, y, t):
        raise NotImplementedError()
