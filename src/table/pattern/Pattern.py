'''
Created on 7 May 2017

@author: Janion
'''


class Pattern(object):

    def __init__(self, name, redFunction, greenFunction, blueFunction):
        self.name = name
        self.redFunction = redFunction
        self.greenFunction = greenFunction
        self.blueFunction = blueFunction
        
    def getName(self):
        return self.name
    
    def getRedFunction(self):
        return self.redFunction

    def getGreenFunction(self):
        return self.greenFunction

    def getBlueFunction(self):
        return self.blueFunction
