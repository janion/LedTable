'''
Created on 7 May 2017

@author: Janion
'''

from time import sleep

from table.led.PixelWriterFactory import PixelWriter2DFactory
from neopixel import Adafruit_NeoPixel as NeoPixel
from table.led.PixelUpdaterPi import PixelUpdater, PixelUpdaterThread
from table.led.builtin.text.TextPixelWriter import PixelWriter
from table.web.IpAddressGetter import getIpAddress
from table.web.WebServer import WebServer, WebServerThread
from table.pattern.PatternManager import PatternManager
from table.Constants import *


if __name__ == '__main__':
    writerFactory = PixelWriter2DFactory(LED_COUNT_X * LED_COUNT_Y)
    writer = PixelWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D, getIpAddress())
    strip = NeoPixel(LED_COUNT_X * LED_COUNT_Y, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()

    updater = PixelUpdater(writer, strip)
    updaterThread = PixelUpdaterThread(updater)

    patterns = PatternManager(writerFactory)
    server = WebServer(updater, writerFactory, patterns)
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
