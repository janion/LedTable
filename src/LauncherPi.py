'''
Created on 7 May 2017

@author: Janion
'''

# from neopixel import Adafruit_NeoPixel as NeoPixel
from table.led.MockNeoPixel import Adafruit_NeoPixel as NeoPixel
from table.led.PixelWriter import PixelWriter1D
from table.led.PixelUpdaterPi import PixelUpdater, PixelUpdaterThread
from table.pattern.Pattern import Pattern

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


if __name__ == '__main__':
    writer = PixelWriter1D(LED_COUNT)
    writer.setPattern(Pattern("NAME", "127 * (sin(t + (x / 50)) + 1)", "0", "0"))
    strip = NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()

    updater = PixelUpdater(writer, strip)
    updaterThread = PixelUpdaterThread(updater)
    updaterThread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        updater.stop()
        updater.join()
