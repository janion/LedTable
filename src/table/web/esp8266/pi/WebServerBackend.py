from threading import Thread
from serial import Serial
from time import sleep


class WebServerThread(Thread):

    def __init__(self, service):
        Thread.__init__(self, target=service.serverLoop, name="WebServerThread")
        self.setDaemon(True)


class WebServerBackend(object):

    PORT = "/dev/ttyUSB0"
    BAUD = 115200
    ADD = "ADD"
    SET = "SET"
    GET_PATTERNS = "GET"
    GET_BUILTINS = "BLT"
    GET_CURRENT = "CUR"
    DEL = "DEL"
    VALID = "VAL"
    INVALID = "INV"
    PATTERN_END = "#"
    SEPARATOR = ","
    END = "\n"

    def __init__(self, pixelUpdater, writerFactory, patternManager, connection=None):
        self.updater = pixelUpdater
        self.writerFactory = writerFactory
        self.patterns = patternManager
        if connection is not None:
            self.connection = connection
        else:
            self.connection = Serial(self.PORT, self.BAUD)

    def serverLoop(self):
        while True:
            line = self._readLine()
            start = line[ : 3]

            if start == self.ADD:
                pattern = line[3 : ].replace(self.END, "").split(self.SEPARATOR)
                self._addPattern(pattern[0], pattern[1], pattern[2], pattern[3])
            elif start == self.SET:
                name = line[3 : ].replace(self.END, "")
                self._setPattern(name)
            elif start == self.DEL:
                name = line[3 : ].replace(self.END, "")
                self._removePattern(name)
            elif start == self.GET_PATTERNS:
                self._sendPatterns()
            elif start == self.GET_BUILTINS:
                self._sendBuiltinPatterns()
            elif start == self.GET_CURRENT:
                self._sendCurrentPattern()

    def _readLine(self):
        line = ""
        while self.connection.inWaiting() == 0:
            sleep(0.001)

        while self.connection.inWaiting() > 0:
            line += self.connection.read()
            if line[-1] == self.END:
                return line

    def _addPattern(self, name, red, green, blue):
        if self.patterns.addPattern(name, red, green, blue):
            self.connection.write(self.VALID)
        else:
            self.connection.write(self.INVALID)
        self.connection.write(self.END)

    def _setPattern(self, name):
        self.patterns.setPattern(name)
        writer = self.patterns.getCurrentWriter()
        self.updater.setPixelWriter(writer)

    def _removePattern(self, name) :
        self.patterns.removePattern(name)

    def _sendPatterns(self) :
        for p in self.patterns.getPatterns():
            self.connection.write(p.getName())
            self.connection.write(self.SEPARATOR)
            self.connection.write(p.getRedFunctionString())
            self.connection.write(self.SEPARATOR)
            self.connection.write(p.getGreenFunctionString())
            self.connection.write(self.SEPARATOR)
            self.connection.write(p.getBlueFunctionString())
            self.connection.write(self.END)
        self.connection.write(self.PATTERN_END)
        self.connection.write(self.END)

    def _sendCurrentPattern(self):
        self.connection.write(self.patterns.getCurrentPatternName())
        self.connection.write(self.END)

    def _sendBuiltinPatterns(self) :
        names = self.patterns.getBuiltinPatternsManager().getPatternNames()
        for i in range(len(names)):
            self.connection.write(names[i])
            if i < len(names) - 1:
                self.connection.write(self.SEPARATOR)
        self.connection.write(self.END)
