from Function import Function


class SerialConnection(object):

    BAUD = 115200
    ADD = "ADD"
    SET = "SET"
    GET_PATTERNS = "GET"
    GET_BUILTINS = "BLT"
    GET_CURRENT = "CUR"
    DEL = "DEL"
    VALID = "VAL"
    PATTERN_END = "#"
    SEPARATOR = ","
    END = "\n"

    def setPattern(self, name):
        print(self.SET)
        print(name)
        print(self.END)

    def removePattern(self, name):
        print(self.DEL)
        print(name)
        print(self.END)

    def addPattern(self, name, red, green, blue):
        print(self.ADD)
        print(name)
        print(self.SEPARATOR)
        print(red)
        print(self.SEPARATOR)
        print(green)
        print(self.SEPARATOR)
        print(blue)

        return input(self.END).startswith(self.VALID)

    def getPatterns(self):
        print(self.GET_PATTERNS)
        print(self.END)

        patterns = []
        while True:
            pattern = input("").split(self.SEPARATOR)
            if pattern[0] == self.PATTERN_END:
                break
            patterns.append(Function(pattern[0], pattern[1], pattern[2], pattern[3]))

        return patterns

    def getBuiltinPatternNames(self):
        return input(self.GET_BUILTINS + self.END).split(self.SEPARATOR)

    def getCurrentPatternName(self):
        return input(self.GET_CURRENT + self.END)
