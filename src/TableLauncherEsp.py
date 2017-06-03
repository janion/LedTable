'''
Created on 7 May 2017

@author: Janion
'''

from time import sleep

from table.led.PixelWriterFactory import PixelWriter2DFactory
from neopixel import Adafruit_NeoPixel as NeoPixel
# from table.led.MockNeoPixel import Adafruit_NeoPixel as NeoPixel
from table.led.PixelUpdaterPi import PixelUpdater, PixelUpdaterThread
from table.web.esp8266.pi.WebServerBackend import WebServerBackend, WebServerThread
from table.pattern.Pattern import Pattern
from table.pattern.PatternManager import PatternManager
from table.Constants import *


if __name__ == '__main__':
    writerFactory = PixelWriter2DFactory(LED_COUNT_X * LED_COUNT_Y)
    writer = writerFactory.createPixelWriter(Pattern("NAME", "50", "50", "50"))
    strip = NeoPixel(LED_COUNT_X * LED_COUNT_Y, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()

    updater = PixelUpdater(writer, strip)
    updaterThread = PixelUpdaterThread(updater)

    patterns = PatternManager(writerFactory)
    server = WebServerBackend(updater, writerFactory, patterns)
    serverThread = WebServerThread(server)

    updaterThread.start()
    serverThread.start()

    try:
        while True:
            sleep(0.01)
    except KeyboardInterrupt:
        print "Stopping"
        updaterThread.stop()
        updaterThread.join()
