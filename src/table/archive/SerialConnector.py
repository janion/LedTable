'''
Created on 7 May 2017

@author: Janion
'''

from serial import Serial

class SerialConnector(object):

    def makeConnection(self, baudrate, port=None):
        if port != None:
            try:
                return Serial(port, baudrate)
            except:
                pass
        else:
            for x in xrange(9):
                try:
                    return Serial('COM%d' %x, baudrate)
                except:
                    pass
        return None
    
    