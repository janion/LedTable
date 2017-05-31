from table.Constants import LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D
from table.led.builtin.rainbow.RainbowSwipePixelWriter import PixelWriter as SwipeWriter
from table.led.builtin.rainbow.RasterDotRainbowFadePixelWriter import PixelWriter as DotFadeWriter
from table.led.builtin.rainbow.RasterDotRainbowPixelWriter import PixelWriter as DotWriter
from table.led.builtin.rainbow.RollingRainbowPixelWriter import PixelWriter as RollWriter
from table.led.builtin.rainbow.SolidRainbowPixelWriter import PixelWriter as SolidWriter


class BuiltinFunctionManager(object):

    def __init__(self):
        # TODO: Better names
        self.writers = {"Dot raster fade": DotFadeWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        "Dot raster": DotWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        "Rainbow roll": RollWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        "Solid rainbow fade": SolidWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        "Rainbow swipe": SwipeWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D)
                        }

    def getPatternNames(self):
        return self.writers.keys()

    def getWriter(self, name):
        return self.writers.get(name)
