from time import sleep


class Adafruit_NeoPixel(object):

    def __init__(self, ledCount, ledPin, ledFreq, ledDma, ledInvert, ledBrightness):
        pass

    def begin(self):
        pass

    def setPixelColor(self, position, colour):
        pass

    def show(self):
        print "Showing"
        sleep(1)


class Color(object):

    def __init__(self, red, green, blue):
        pass
