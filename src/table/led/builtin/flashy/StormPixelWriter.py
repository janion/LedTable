from table.led.PixelWriter import PixelWriter2D
from table.led.configure.custom.CustomConfigurer import CustomConfigurer
from table.led.configure.custom.item.NumberItem import NumberItem
from random import randint, uniform


class Lightning(object):

    MAX_BRIGHTNESS = 180

    def __init__(self, probability, fadeTime):
        self.startTime = -fadeTime
        self.probability = probability
        self.fadeTime = fadeTime
        self.endTime = self.startTime + self.fadeTime
        self.factor = 0

    def tick(self, t):
        if uniform(0, 1) < self.probability:
            self.startTime = t - self.fadeTime
            self.endTime = self.startTime + self.fadeTime
        numerator = (t - self.endTime) * (t - self.endTime)
        denominator = self.fadeTime * self.fadeTime
        self.factor = min(numerator / denominator, 1)

    def getBrightness(self):
        return self.MAX_BRIGHTNESS * (1 - self.factor)


class RainDrop(object):

    PROFILE_HEAD_LENGTH = 1
    PROFILE_TAIL_LENGTH = 5
    RED = 20
    GREEN = 180
    BLUE = 255

    def __init__(self, x, y, t, fallSpeed):
        self.startY = y
        self.x = x
        self.y = y
        self.startTime = t
        self.fallSpeed = fallSpeed

    def tick(self, t):
        self.y = self.startY - (self.fallSpeed * (t - self.startTime))

    def getX(self):
        return self.x

    def isExpired(self):
        return self.y < -self.PROFILE_TAIL_LENGTH

    def calculate(self):
        cells = {}
        for y in range(1, self.PROFILE_HEAD_LENGTH):
            factor = 1 - (float(y) / self.PROFILE_HEAD_LENGTH)
            cells[int(self.y) - y] = (self.RED * factor, self.GREEN * factor, self.BLUE * factor)

        for y in range(self.PROFILE_TAIL_LENGTH):
            factor = 1 - (float(y) / self.PROFILE_TAIL_LENGTH)
            cells[int(self.y) + y] = (self.RED * factor, self.GREEN * factor, self.BLUE * factor)

        return cells


class PixelWriter(PixelWriter2D):

    NAME = "STORM"

    TIME_BETWEEN_DROPS = 0.0
    FALL_SPEED = 25.0
    FREQUENCY_KEY = "frequency"
    FREQUENCY_TITLE = "Rain drops per second:"
    FALL_SPEED_KEY = "fallSpeed"
    FALL_SPEED_TITLE = "Fall speed:"

    LIGHTNING_PROBABILITY = 0.01
    LIGHTNING_FADE_TIME = 0.5

    def __init__(self, ledCountX, ledCountY, mode):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)

        self._createConfiguration()

        self.lastIncrement = 0
        self.rainDrops = []
        self.timeBetweenDrops = self.TIME_BETWEEN_DROPS
        self.fallSpeed = self.FALL_SPEED
        self.cells = [[(0, 0, 0) for y in range(self.ledCountY)] for x in range(self.ledCountX)]
        self.lightning = Lightning(self.LIGHTNING_PROBABILITY, self.LIGHTNING_FADE_TIME)

    def _createConfiguration(self):
        frequencyItem = NumberItem(self.FREQUENCY_TITLE, self.FREQUENCY_KEY, self.setDropsPerSecond, self.getDropsPerSecond)
        fallSpeedItem = NumberItem(self.FALL_SPEED_TITLE, self.FALL_SPEED_KEY, self.setFallSpeed, self.getFallSpeed)
        self.configurer = CustomConfigurer(self, self.NAME, [frequencyItem, fallSpeedItem])

    def _tick(self, t):
        self.lightning.tick(t)
        self.cells = [[(0, 0, 0) for y in range(self.ledCountY)] for x in range(self.ledCountX)]
        for i in range(len(self.rainDrops)):
            drop = self.rainDrops[i]
            drop.tick(t)
            if drop.isExpired():
                self.rainDrops[i] = None
            else:
                x = drop.getX()
                for (y, brightness) in drop.calculate().iteritems():
                    if 0 <= y < self.ledCountY and brightness[2] > self.cells[x][y][2]:
                        self.cells[x][y] = brightness

        for __ in range(self.rainDrops.count(None)):
            self.rainDrops.remove(None)

        if (t - self.lastIncrement) >= self.timeBetweenDrops:
            x = randint(0, self.ledCountX - 1)
            self.rainDrops.append(RainDrop(x, self.ledCountY - 1, t, self.fallSpeed))
            self.lastIncrement = t

    def _evaluateCell(self, x, y, t):
        colour = self.cells[x][self.ledCountY - (y + 1)]
        flash = self.lightning.getBrightness()
        return int(max(flash, colour[0])), int(max(flash, colour[1])), int(max(flash, colour[2]))

    def reset(self, t):
        super(PixelWriter, self).reset(t)
        self.lastIncrement = t
        self.rainDrops = []

    def setDropsPerSecond(self, dropsPerSecond):
        self.timeBetweenDrops = 1 / float(dropsPerSecond)

    def getDropsPerSecond(self):
        return int(round(1.0 / self.timeBetweenDrops))

    def setFallSpeed(self, fallSpeed):
        self.fallSpeed = float(fallSpeed)

    def getFallSpeed(self):
        return self.fallSpeed