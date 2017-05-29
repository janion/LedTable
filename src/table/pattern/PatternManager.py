'''
Created on 7 May 2017

@author: Janion
'''

from table.pattern.Pattern import Pattern
from table.pattern.FileIO import PatternReader, PatternWriter
from table.led.builtin.BuiltinFunctionManager import BuiltinFunctionManager


class PatternManager(object):
    
    DEFAULT_PATTERN = Pattern("Default", "127", "127", "127")
    DEFAULT_PATTERN_FILE_NAME = "patterns.csv"

    def __init__(self, writerFactory, patternFileName=None):
        if patternFileName is not None:
            self.patternFileName = patternFileName
        else:
            self.patternFileName = self.DEFAULT_PATTERN_FILE_NAME

        self.writerFactory = writerFactory
        self.fileReader = PatternReader()
        self.fileWriter = PatternWriter()
        self.patterns = self.fileReader.readPatterns(self.patternFileName)
        self.builtins = BuiltinFunctionManager()

        if len(self.patterns) > 0:
            self.setPattern(self.patterns[0].getName())
        else:
            self.currentPatternName = self.DEFAULT_PATTERN.getName()
            self.currentWriter = self.writerFactory.createPixelWriter(self.DEFAULT_PATTERN)

    def getCurrentPatternName(self):
        return self.currentPatternName
    
    def getPatterns(self):
        return self.patterns

    def getBuiltinPatternsManager(self):
        return self.builtins

    def setPattern(self, name):
        self.currentPatternName = name

        # Check builtins
        for builtinName in self.builtins.getPatternNames():
            if builtinName == name:
                self.currentWriter = self.builtins.getWriter(name)
                return

        # Check custom patterns
        for pattern in self.patterns:
            if pattern.getName() == name:
                self.currentWriter = self.writerFactory.createPixelWriter(pattern)
                break

    def addPattern(self, name, redFunction, greenFunction, blueFunction):
        pattern = Pattern(name, redFunction, greenFunction, blueFunction)
        if pattern.isValid:
            self.patterns.append(pattern)
            self.fileWriter.writePatterns(self.patternFileName, self.patterns)
            if len(self.patterns) == 1:
                self.setPattern(name)
            return True
        return False

    def removePattern(self, name):
        for i in range(len(self.patterns)):
            pattern = self.patterns[i]
            if pattern.getName() == name:
                self.patterns.remove(pattern)

                if name == self.currentPatternName:
                    if len(self.patterns) > 0:
                        self.setPattern(self.patterns[0])
                    else:
                        self.currentPatternName = self.DEFAULT_PATTERN.getName()
                        self.currentWriter = self.writerFactory.createPixelWriter(self.DEFAULT_PATTERN)
                        
                self.fileWriter.writePatterns(self.patternFileName, self.patterns)
                break

    def getWriter(self):
        return self.currentWriter
