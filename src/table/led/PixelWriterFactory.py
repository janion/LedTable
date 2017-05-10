from table.led.PixelWriter import PixelWriter1D, PixelWriter2D


class PixelWriter1DFactory(object):

    def __init__(self, ledCount):
        self.ledCount = ledCount
    
    def createPixelWriter(self, pattern):
        return PixelWriter1D(self.ledCount, pattern)


class PixelWriter2DFactory(object):

    def __init__(self, ledCountX, ledCountY, mode):
        self.ledCountX = ledCountX
        self.ledCountY = ledCountY
        self.mode = mode

    def createPixelWriter(self, pattern):
        return PixelWriter2D(self.ledCountX, self.ledCountY, pattern, self.mode)
