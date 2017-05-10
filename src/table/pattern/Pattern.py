'''
Created on 7 May 2017

@author: Janion
'''
from EquationParser import Equation


class Pattern(object):

    def __init__(self, name, redFunction, greenFunction, blueFunction):
        self.name = name
        self.redFunctionString = redFunction
        self.greenFunctionString = greenFunction
        self.blueFunctionString = blueFunction
        self.redFunction = self._createEquationAndValidate(redFunction)
        self.greenFunction = self._createEquationAndValidate(greenFunction)
        self.blueFunction = self._createEquationAndValidate(blueFunction)

        self.isValid = None in [self.redFunction, self.greenFunction, self.blueFunction]
        
    def isValid(self):
        return self.isValid

    def getName(self):
        return self.name
    
    def getRedFunctionString(self):
        return self.redFunctionString

    def getGreenFunctionString(self):
        return self.greenFunctionString

    def getBlueFunctionString(self):
        return self.blueFunctionString

    def _createEquationAndValidate(self, functionString):
        try:
            return Equation(functionString)
        except RuntimeError:
            return None
