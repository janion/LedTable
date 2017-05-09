'''
Created on 7 May 2017

@author: Janion
'''

from PixelWriter import PixelWriter1D
from PixelUpdaterByte import PixelUpdater

if __name__ == '__main__':
    writer = PixelWriter1D(60)
    writer.setRedFunction("127 * (sin(t + (x / 50)) + 1)")
#     writer.setGreenFunction("t")
#     writer.setBlueFunction("x")
    updater = PixelUpdater(writer)
    updater.start()