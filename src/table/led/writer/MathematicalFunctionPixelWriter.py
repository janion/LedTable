from table.led.writer.PixelWriter import PixelWriter2D


class MathematicalFunctionPixelWriter(PixelWriter2D):

    def __init__(self, ledCountX, ledCountY, mode, pattern):
        super(MathematicalFunctionPixelWriter, self).__init__(ledCountX, ledCountY, mode, pattern.getName())

        if pattern is not None:
            self.rFunc = pattern.getRedFunction()
            self.gFunc = pattern.getGreenFunction()
            self.bFunc = pattern.getBlueFunction()

    def _evaluateCell(self, x, y, t):
        return (int(self.rFunc.evaluate(x, y, t)[0]),
                int(self.gFunc.evaluate(x, y, t)[0]),
                int(self.bFunc.evaluate(x, y, t)[0])
                )
