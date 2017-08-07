'''
Created on 7 May 2017

@author: Janion
'''

from table.Constants import *
# from neopixel import Adafruit_NeoPixel as NeoPixel
from table.led.MockNeoPixel import Adafruit_NeoPixel as NeoPixel
from table.led.MockPixelUpdater import PixelUpdater, PixelUpdaterThread
from table.led.writer.MathematicalFunctionPixelWriterFactory import MathematicalFunctionPixelWriterFactory
# from table.web.WebServer import WebServer, WebServerThread
from table.led.builtin.snake.SnakePixelWriter import SnakePixelWriter as SnakeWriter
from table.led.builtin.automata.gameoflife.GameOfLifePixelWriter import GameOfLifePixelWriter as GolWriter
from table.led.builtin.automata.wolfram.WolframRulePixelWriter import WolframRulePixelWriter as WolframWriter
from table.led.builtin.flashy.StarFadePixelWriter import StarFadePixelWriter as StarWriter
from table.led.builtin.rainbow.RainbowSwipePixelWriter import RainbowSwipePixelWriter as SwipeWriter
# from table.led.builtin.rainbow.SolidRainbowPixelWriter import PixelWriter as SolidFadeWriter
from table.led.builtin.rainbow.RollingRainbowPixelWriter import RollingRainbowPixelWriter as RollingRainbowWriter
from table.led.builtin.rainbow.SolidColourPixelWriter import SolidColourPixelWriter as SolidColourWriter
from table.led.builtin.text.TextPixelWriter import TextPixelWriter as TextWriter
from table.led.builtin.flashy.StormPixelWriter import StormPixelWriter as StormWriter
# from table.led.PixelUpdaterPi import PixelUpdater, PixelUpdaterThread
from table.pattern.Pattern import Pattern
from table.pattern.PatternManager import PatternManager

if __name__ == '__main__':
    writerFactory = MathematicalFunctionPixelWriterFactory(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D)
    writer = writerFactory.createPixelWriter(Pattern("NAME", "127 * (sin(t + (x / 5) + (y / 5)) + 1)",
                                                     "127 * (cos(t + (x / 5) + (y / 5)) + 1)",
                                                     "127 * (sin(t + (x / 5) + (6.243 / 1.5) + (y / 5)) + 1)"
                                                     ))
    strip = NeoPixel(LED_COUNT_X * LED_COUNT_Y, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()

    patterns = PatternManager(writerFactory)

    # writer = SnakeWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D)
    # writer = GolWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D)
    # writer = WolframWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D, 90)
    # writer = StarWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D)
    # writer = SolidFadeWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D)
    # writer = RollingRainbowWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D)
    # writer = SolidColourWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D)
    writer = TextWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D)
    writer.setTextContent("Some scrolling text")
    writer.setColumnPerSeconds(12)
    writer.setColour("#22ff88")
    writer.setUseRainbowColour(None)
    # writer = SwipeWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D)
    # writer.setSwipeTime(5)
    # writer = StormWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D)
    # writer.setFallSpeed(1)
    # writer.setDropsPerSecond(1)
    updater = PixelUpdater(writer, strip)
    updaterThread = PixelUpdaterThread(updater)

    updaterThread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        updaterThread.stop()
        updaterThread.join()
