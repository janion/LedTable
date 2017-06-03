from time import sleep

from machine import UART as Serial

from table.web.esp8266.microcontroller.Function import Function


class SerialConnection(object):

    BAUD = 115200
    ADD = "ADD"
    SET = "SET"
    GET_PATTERNS = "GET"
    GET_BUILTINS = "BLT"
    DEL = "DEL"
    VALID = "VAL"
    PATTERN_END = "#"
    SEPARATOR = ","
    END = "\n"

    def __init__(self):
        self.connection = Serial(1, self.BAUD)

    def setPattern(self, name):
        self.connection.write(self.SET)
        self.connection.write(name)
        self.connection.write(self.END)

    def removePattern(self, name):
        self.connection.write(self.DEL)
        self.connection.write(name)
        self.connection.write(self.END)

    def addPattern(self, name, red, green, blue):
        self.connection.write(self.ADD)
        self.connection.write(name)
        self.connection.write(self.SEPARATOR)
        self.connection.write(red)
        self.connection.write(self.SEPARATOR)
        self.connection.write(green)
        self.connection.write(self.SEPARATOR)
        self.connection.write(blue)
        self.connection.write(self.END)

        while not self.connection.any():
            sleep(0.001)
        return self.connection.readline().startswith(self.VALID)

    def getPatterns(self):
        self.connection.write(self.GET_PATTERNS)
        self.connection.write(self.END)

        patterns = []
        more = True
        while True:
            while not self.connection.any():
                sleep(0.001)
            pattern = self.connection.readline().split(self.SEPARATOR)
            if pattern[0] == self.PATTERN_END:
                break
            patterns.append(Function(pattern[0], pattern[1], pattern[2], pattern[3]))

        return patterns

    def getBuiltinPatternNames(self):
        self.connection.write(self.GET_BUILTINS)
        self.connection.write(self.END)

        while not self.connection.any():
            sleep(0.001)

        return self.connection.readline().split(self.SEPARATOR)
