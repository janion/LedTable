'''
Created on 6 May 2017

@author: Janion
'''


class PixelWriter1D(object):

    def __init__(self, ledCount, pattern):
        self.data = [(0, 0, 0) for x in range(ledCount)]
        self.ledCount = ledCount
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
                for y in range(self.ledCountY):
                    self.data[(x * self.ledCountX) + y] = (int(self.rFunc.evaluate(x, y, t)[0]),
                                                           int(self.gFunc.evaluate(x, y, t)[0]),
                                                           int(self.bFunc.evaluate(x, y, t)[0])
                                                           )
        elif self.mode == self.ZIG_ZAG:
            for x in range(self.ledCountX):
                if (x % 2) == 0:
                    for y in range(self.ledCountY):
                        self.data[(x * self.ledCountX) + y] = (int(self.rFunc.evaluate(x, y, t)[0]),
                                                               int(self.gFunc.evaluate(x, y, t)[0]),
                                                               int(self.bFunc.evaluate(x, y, t)[0])
                                                               )
                else:
                    for y in range(self.ledCountY - 1, -1, -1):
                        index = (x * self.ledCountX) + (self.ledCountY - (1 + y))
                        self.data[index] = (int(self.rFunc.evaluate(x, y, t)[0]),
                                            int(self.gFunc.evaluate(x, y, t)[0]),
                                            int(self.bFunc.evaluate(x, y, t)[0])
                                            )

        return self.data
