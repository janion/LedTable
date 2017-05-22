'''
Created on 7 May 2017

@author: Janion
'''

# from neopixel import Adafruit_NeoPixel as NeoPixel
from table.led.MockNeoPixel import Adafruit_NeoPixel as NeoPixel
from table.led.PixelWriterFactory import PixelWriter2DFactory
from table.led.MockPixelUpdater import PixelUpdater, PixelUpdaterThread
# from table.led.PixelUpdaterPi import PixelUpdater, PixelUpdaterThread
from table.pattern.Pattern import Pattern
from table.pattern.PatternManager import PatternManager
from table.led.PixelWriter import PixelWriter2D
# from table.web.WebServer import WebServer, WebServerThread
from table.web.MockWebServer import WebServer, WebServerThread

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

SIZE = 10

if __name__ == '__main__':
    writerFactory = PixelWriter2DFactory(SIZE, SIZE, PixelWriter2D.ZIG_ZAG)
    writer = writerFactory.createPixelWriter(Pattern("NAME", "127 * (sin(t + (x / 5) + (y / 5)) + 1)",
                                                     "127 * (cos(t + (x / 5) + (y / 5)) + 1)",
                                                     "127 * (sin(t + (x / 5) + (6.243 / 1.5) + (y / 5)) + 1)"
                                                     ))
    strip = NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()

    patterns = PatternManager()

    updater = PixelUpdater(writer, strip)
    updaterThread = PixelUpdaterThread(updater)
    server = WebServer(updater, writerFactory, patterns)
    # serverThread = WebServerThread(server)

    updaterThread.start()
    # serverThread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        updaterThread.stop()
        updaterThread.join()
