'''
Created on 7 May 2017

@author: Janion
'''

from threading import Lock, Thread
from time import time, sleep
from table.led.MockNeoPixel import Color
# from neopixel import Color


class PixelUpdaterThread(Thread):

    def __init__(self, updater):
        Thread.__init__(self, target=updater.updateLoop, name="PixelUpdaterThread")
        self.updater = updater

    def stop(self):
        self.updater.stop()


class PixelUpdater(object):
    
    def __init__(self, writer, strip):
        self.writer = writer
        self.strip = strip
        self.writerLock = Lock()
        self.stopped = False
    
    def setPixelWriter(self, writer):
        with self.writerLock:
            self.writer = writer
        print "Pixel writer set"

    def stop(self):
        self.stopped = True

    def updateLoop(self):
        startTime = time()
        while not self.stopped:
            with self.writerLock:
                data = self.writer.getPixelData(time() - startTime)
                
            for x in range(len(data)):
                datum = data[x]
                self.strip.setPixelColor(x, Color(datum[0], datum[1], datum[2]))

            self.strip.show()
