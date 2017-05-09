'''
Created on 7 May 2017

@author: Janion
'''

class Pattern(object):

    def __init__(self, name, function):
        self.name = name
        self.function = function
        
    def getName(self):
        return self.name
    
    def getFunction(self):
        return self.function
        