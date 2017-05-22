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
        self.reader = PatternReader()
        self.writer = PatternWriter()
        self.patterns = self.reader.readPatterns(self.patternFileName)
        self.builtins = BuiltinFunctionManager()

        if len(self.patterns) > 0:
            self.currentPattern = self.patterns[0]
        else:
            self.currentPattern = self.DEFAULT_PATTERN

    def getCurrentPatternName(self):
        return self.currentPattern.getName()
    
    def getCurrentPattern(self):
        return self.currentPattern
    
    def getPatterns(self):
        return self.patterns

    def getBuiltinPatternsManager(self):
        return self.builtins

    def setPattern(self, name):
        # TODO: Check if pattern name in custon or builtins
        for pattern in self.patterns:
            if pattern.getName() == name:
                self.currentPattern = pattern
                break

    def addPattern(self, name, redFunction, greenFunction, blueFunction):
        pattern = Pattern(name, redFunction, greenFunction, blueFunction)
        if pattern.isValid:
            if len(self.patterns) == 0:
                self.currentPattern = pattern
            self.patterns.append(pattern)
            self.writer.writePatterns(self.patternFileName, self.patterns)

    def removePattern(self, name):
        for i in range(len(self.patterns)):
            pattern = self.patterns[i]
            if pattern.getName() == name:
                self.patterns.remove(pattern)

                if pattern == self.currentPattern:
                    if len(self.patterns) > 0:
                        self.setPattern(self.patterns[0])
                    else:
                        self.setPattern(self.DEFAULT_PATTERN)
                        
                self.writer.writePatterns(self.patternFileName, self.patterns)
                break

    def getWriter(self):
        # TODO: Get builtin pattern writer if set
        return self.writerFactory.createPixelWriter(self.currentPattern)
