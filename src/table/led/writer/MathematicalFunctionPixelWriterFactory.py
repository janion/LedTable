from table.led.writer.MathematicalFunctionPixelWriter import MathematicalFunctionPixelWriter


class MathematicalFunctionPixelWriterFactory(object):

    def __init__(self, ledCountX, ledCountY, mode):
        self.ledCountX = ledCountX
        self.ledCountY = ledCountY
        self.mode = mode

    def createPixelWriter(self, pattern):
        return MathematicalFunctionPixelWriter(self.ledCountX, self.ledCountY, self.mode, pattern)
