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
import table.web.WebServer as WebServer
from table.pattern.PatternManager import PatternManager
from table.web.WifiConnectionSetup import WifiConnectionSetup
from table.hardware.PhysicalButtons import PhysicalButtons
from table.Constants import *


def stop(updaterThread):
    updaterThread.stop()
    updaterThread.join()
    os.popen("sudo shutdown -h now")


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
    # WebServer.initResponseCreator(updater, writerFactory, patterns)
    # serverThread = WebServer.WebServerThread()

    server = WebServer.WebServer(updater, writerFactory, patterns)
    serverThread = WebServer.WebServerThread(server)

    updaterThread.start()
    serverThread.start()

    PhysicalButtons(lambda: updater.setPixelWriter(writer), lambda: stop(updaterThread))

    try:
        while True:
            sleep(0.01)
    except KeyboardInterrupt:
        print("Stopping")
        updaterThread.stop()
        updaterThread.join()
        server.stop()
        #serverThread.stop()
        #serverThread.join()
