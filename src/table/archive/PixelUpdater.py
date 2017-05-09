'''
Created on 7 May 2017

@author: Janion
'''

from threading import Lock, Thread
from time import time, sleep
from SerialConnector import SerialConnector

class PixelUpdater(Thread):
    
    DATA_END = ""
    DATUM_FORMAT = "%03d%03d%03d"
    
    def __init__(self, writer):
        Thread.__init__(self, target=self.updateLoop)
        self.writer = writer
        self.connection = SerialConnector().makeConnection(115200)
        self.writerLock = Lock()
    
    def setPixelWriter(self, writer):
        with self.writerLock:
            self.writer = writer

    def updateLoop(self):
        startTime = time()
#         while(True):
        while(self.connection != None and self.connection.isOpen()):
            with self.writerLock:
                data = self.writer.getPixelData(time() - startTime)
                
            dataString = ""
            for datum in data:
                dataString += self.DATUM_FORMAT % datum
            
            dataString += self.DATA_END
            print dataString
#             sleep(1)

            self.connection.write(dataString)
        