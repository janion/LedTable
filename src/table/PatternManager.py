'''
Created on 7 May 2017

@author: Janion
'''

from Pattern import Pattern

class PatternManager(object):
    
    DEFAULT_PATTERN = Pattern("Default", "127")

    def __init__(self, patternFileName):
        self.patternFileName = patternFileName
        # TODO read from file
        self.patterns = []
        self.addPattern("one", "x")
        self.addPattern("two", "2 * x")
        self.addPattern("three", "3 * x")
    
    def getCurrentPattern(self):
        return self.currentPattern
    
    def getPatterns(self):
        return self.patterns

    def setPattern(self, name):
        for pattern in self.patterns:
            if pattern.getName() == name:
                self.currentPattern = pattern
                break

    def addPattern(self, name, function):
        pattern = Pattern(name, function)
        if len(self.patterns) == 0:
            self.currentPattern = pattern
        self.patterns.append(pattern)

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
                # TODO write to file
                break
        
