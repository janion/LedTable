'''
Created on 7 May 2017

@author: Janion
'''

from threading import Lock, Thread
from time import time


def _correctColour(colour):
    return colour[1], colour[0], colour[2]


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
        self.startTime = time()
    
    def setPixelWriter(self, writer):
        with self.writerLock:
            self.writer = writer
            self.startTime = time()
            self.writer.reset()
        print "Pixel writer set"

    def setBrightness(self, val):
        with self.writerLock:
            self.strip.setBrightness(val)

    def stop(self):
        self.stopped = True

    def updateLoop(self):
        while not self.stopped:
            with self.writerLock:
                data = self.writer.getPixelData(time() - self.startTime)
                
            for x in range(len(data)):
                datum = _correctColour(data[x])
                self.strip.setPixelColorRGB(x, datum[0], datum[1], datum[2])

            self.strip.show()
