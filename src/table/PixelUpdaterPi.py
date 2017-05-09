'''
Created on 7 May 2017

@author: Janion
'''

from threading import Lock, Thread
from time import time, sleep
from neopixel import Color

class PixelUpdater(Thread):
    
    def __init__(self, writer, strip):
        Thread.__init__(self, target=self.updateLoop)
        self.writer = writer
        self.strip = strip
        self.writerLock = Lock()
        self.stopped = False
    
    def setPixelWriter(self, writer):
        with self.writerLock:
            self.writer = writer
    
    def stop(self):
        self.stopped = True

    def updateLoop(self):
        startTime = time()
        while(not self.stopped):
            with self.writerLock:
                data = self.writer.getPixelData(time() - startTime)
                
            for x in range(len(data)):
                datum = data[x]
                self.strip.setPixelColor(x, Color(datum[0], datum[1], datum[2]))

            self.strip.show()
                
        
