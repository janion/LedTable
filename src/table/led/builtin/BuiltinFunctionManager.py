from table.Constants import LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D
from table.led.builtin.rainbow.RainbowSwipePixelWriter import PixelWriter as SwipeWriter
from table.led.builtin.rainbow.RasterDotRainbowFadePixelWriter import PixelWriter as DotFadeWriter
from table.led.builtin.rainbow.RasterDotRainbowPixelWriter import PixelWriter as DotWriter
from table.led.builtin.rainbow.RollingRainbowPixelWriter import PixelWriter as RollWriter
from table.led.builtin.rainbow.SolidRainbowPixelWriter import PixelWriter as SolidFadeWriter
from table.led.builtin.rainbow.SolidColourPixelWriter import PixelWriter as SolidColourWriter
from table.led.builtin.flashy.StarFadePixelWriter import PixelWriter as StarWriter
from table.led.builtin.flashy.StormPixelWriter import PixelWriter as StormWriter
from table.led.builtin.automata.wolfram.WolframRulePixelWriter import PixelWriter as WolframWriter
from table.led.builtin.automata.gameoflife.GameOfLifePixelWriter import PixelWriter as GolWriter
from table.led.builtin.snake.SnakePixelWriter import PixelWriter as SnakeWriter
from table.led.builtin.text.TextPixelWriter import PixelWriter as TextWriter


class BuiltinFunctionManager(object):

    def __init__(self):
        self.writers = [DotFadeWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        DotWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        RollWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        SolidFadeWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        SolidColourWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        SwipeWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        StarWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        WolframWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D, 30),
                        GolWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        SnakeWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        TextWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        StormWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D)
                        ]
        self.names = []
        for writer in self.writers:
            self.names.append(writer.getName())

    def getPatternNames(self):
        return self.names

    def getWriters(self):
        return self.writers

    def getWriter(self, name):
        for writer in self.writers:
            if name == writer.getName():
                return writer

        return None
