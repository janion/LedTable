'''
Created on 7 May 2017

@author: Janion
'''

from time import sleep

from table.led.PixelWriter import PixelWriter1D, PixelWriter2D
# from neopixel import Adafruit_NeoPixel as NeoPixel
from table.led.MockNeoPixel import Adafruit_NeoPixel as NeoPixel
from table.led.PixelUpdaterPi import PixelUpdater, PixelUpdaterThread
from table.web.WebServer import WebServer, WebServerThread

# LED strip configuration:
LED_SIDE_COUNT = 10
# LED_COUNT      = LED_SIDE_COUNT * LED_SIDE_COUNT      # Number of LED pixels.
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
# LED_BRIGHTNESS = 200     # Set to 0 for darkest and 255 for brightest
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


if __name__ == '__main__':
    writer = PixelWriter1D(LED_COUNT)
    # writer = PixelWriter2D(LED_SIDE_COUNT, LED_SIDE_COUNT, PixelWriter2D.ZIG_ZAG)
    strip = NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()

    updater = PixelUpdater(writer, strip)
    updaterThread = PixelUpdaterThread(updater)

    server = WebServer()
    serverThread = WebServerThread(server)

    updaterThread.start()
    serverThread.start()

    try:
        while True:
            sleep(0.01)
    except KeyboardInterrupt:
        print "Stopping"
        updater.stop()
        updater.join()
