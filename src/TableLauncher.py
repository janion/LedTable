'''
Created on 7 May 2017

@author: Janion
'''

from time import sleep
import os

from table.led.writer.MathematicalFunctionPixelWriterFactory import MathematicalFunctionPixelWriterFactory
from neopixel import Adafruit_NeoPixel as NeoPixel
from table.led.PixelUpdaterPi import PixelUpdater, PixelUpdaterThread
from table.led.builtin.text.TextPixelWriter import TextPixelWriter
from table.web.IpAddressGetter import getIpAddress
from table.web.WebServer import WebServer, WebServerThread
from table.pattern.PatternManager import PatternManager
from table.web.WifiConnectionSetup import WifiConnectionSetup
from table.Constants import *


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))

    WifiConnectionSetup().connect()

    writerFactory = MathematicalFunctionPixelWriterFactory(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D)
    writer = TextPixelWriter(LED_COUNT_X, LED_COUNT_Y, PIXEL_MODE_2D)
    writer.setTextContent(getIpAddress())
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
