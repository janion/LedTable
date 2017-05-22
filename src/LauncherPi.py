'''
Created on 7 May 2017

@author: Janion
'''

# from neopixel import Adafruit_NeoPixel as NeoPixel
from table.led.MockNeoPixel import Adafruit_NeoPixel as NeoPixel
from table.led.PixelWriterFactory import PixelWriter1DFactory
from table.led.PixelUpdaterPi import PixelUpdater, PixelUpdaterThread
from table.pattern.Pattern import Pattern
from table.Constants import *


if __name__ == '__main__':
    writerFactory = PixelWriter1DFactory(LED_COUNT_X * LED_COUNT_Y)
    writer = writerFactory.createPixelWriter(Pattern("NAME", "127 * (sin(t + (x / 5) + (y / 5)) + 1)",
                                                     "127 * (cos(t + (x / 5) + (y / 5)) + 1)",
                                                     "127 * (sin(t + (x / 5) + (6.243 / 1.5) + (y / 5)) + 1)"
                                                     ))
    strip = NeoPixel(LED_COUNT_X * LED_COUNT_Y, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()

    updater = PixelUpdater(writer, strip)
    updaterThread = PixelUpdaterThread(updater)
    updaterThread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        updaterThread.stop()
        updaterThread.join()
