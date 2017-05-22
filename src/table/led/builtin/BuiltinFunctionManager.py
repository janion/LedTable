from table.led.builtin.rainbow.RasterDotRainbowFadePixelWriter import PixelWriter as DotFadeWriter
from table.led.builtin.rainbow.RasterDotRainbowPixelWriter import PixelWriter as DotWriter
from table.led.builtin.rainbow.RollingRainbowPixelWriter import PixelWriter as RollWriter
from table.led.builtin.rainbow.SolidRainbowPixelWriter import PixelWriter as SolidWriter
from table.led.builtin.swipe.RainbowSwipePixelWriter import PixelWriter as SwipeWriter


class BuiltinFunctionManager(object):

    def __init__(self):
        # TODO: Better names
        self.writers = {"Dot raster fade" : DotFadeWriter(),
                        "Dot raster": DotWriter(),
                        "Rainbow roll": RollWriter(),
                        "Solid rainbow fade": SolidWriter(),
                        "Rainbow swipe": SwipeWriter()
                        }

    def getPatternNames(self):
        return self.writers.keys()

    def getWriter(self, name):
        return self.writers.get(name)