from table.Constants import LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D
from table.led.builtin.rainbow.RainbowSwipePixelWriter import RainbowSwipePixelWriter
from table.led.builtin.rainbow.RasterDotRainbowFadePixelWriter import RasterDotRainbowFadePixelWriter
from table.led.builtin.rainbow.RasterDotPixelWriter import RasterDotPixelWriter
from table.led.builtin.rainbow.RollingRainbowPixelWriter import RollingRainbowPixelWriter
from table.led.builtin.rainbow.SolidRainbowPixelWriter import SolidRainbowPixelWriter
from table.led.builtin.rainbow.SolidColourPixelWriter import SolidColourPixelWriter
from table.led.builtin.flashy.StarFadePixelWriter import StarFadePixelWriter
from table.led.builtin.flashy.StormPixelWriter import StormPixelWriter
from table.led.builtin.automata.wolfram.WolframRulePixelWriter import WolframRulePixelWriter
from table.led.builtin.automata.gameoflife.GameOfLifePixelWriter import GameOfLifePixelWriter
from table.led.builtin.snake.SnakePixelWriter import SnakePixelWriter
from table.led.builtin.text.TextPixelWriter import TextPixelWriter


class BuiltinFunctionManager(object):

    def __init__(self):
        self.writers = [RasterDotRainbowFadePixelWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        RasterDotPixelWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        RollingRainbowPixelWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        SolidRainbowPixelWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        SolidColourPixelWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        RainbowSwipePixelWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        StarFadePixelWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        WolframRulePixelWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D, 30),
                        GameOfLifePixelWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        SnakePixelWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        TextPixelWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D),
                        StormPixelWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D)
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
