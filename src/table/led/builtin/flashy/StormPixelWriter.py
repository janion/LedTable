from table.led.writer.PixelWriter import PixelWriter2D
from table.led.configure.custom.CustomConfigurer import CustomConfigurer
from table.led.configure.custom.item.NumberItem import NumberItem
from random import randint, uniform


class Lightning(object):

    MAX_BRIGHTNESS = 180
    FLASH_CHECK_TIME = 0.05

    def __init__(self, probability, fadeTime):
        self.startTime = -fadeTime
        self.probability = probability
        self.fadeTime = fadeTime
        self.endTime = self.startTime + self.fadeTime
        self.factor = 0
        self.lastCheck = 0

    def tick(self, t):
        if t > self.lastCheck + self.FLASH_CHECK_TIME and uniform(0, 1) < self.probability:
            self.startTime = t - self.fadeTime
            self.endTime = self.startTime + self.fadeTime
            self.lastCheck = t
        numerator = (t - self.endTime) * (t - self.endTime)
        denominator = self.fadeTime * self.fadeTime
        self.factor = min(numerator / denominator, 1)

    def reset(self):
        self.lastCheck = 0

    def getBrightness(self):
        return self.MAX_BRIGHTNESS * (1 - self.factor)

    def getFadeTime(self):
        return self.fadeTime

    def setFadeTime(self, fadeTime):
        self.fadeTime = float(fadeTime)

    def getProbability(self):
        return self.probability

    def setProbability(self, probability):
        self.probability = float(probability)


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


class StormPixelWriter(PixelWriter2D):

    NAME = "Storm"

    DROPS_PER_SECOND = 25.0
    FREQUENCY_KEY = "frequency"
    FREQUENCY_TITLE = "Rain drops per second:"

    FALL_SPEED = 25.0
    FALL_SPEED_KEY = "fallSpeed"
    FALL_SPEED_TITLE = "Fall speed:"

    LIGHTNING_PROBABILITY = 0.01
    LIGHTNING_PROBABILITY_KEY = "lightningProbability"
    LIGHTNING_PROBABILITY_TITLE = "Lightning probability:"

    LIGHTNING_FADE_TIME = 0.25
    LIGHTNING_FADE_TIME_KEY = "lightningFadeTime"
    LIGHTNING_FADE_TIME_TITLE = "Lightning fade time:"


    def __init__(self, ledCountX, ledCountY, mode):
        super(StormPixelWriter, self).__init__(ledCountX, ledCountY, mode, self.NAME)

        self.lastIncrement = 0
        self.rainDrops = []
        self.dropsPerSecond = self.DROPS_PER_SECOND
        self.fallSpeed = self.FALL_SPEED
        self.cells = [[(0, 0, 0) for y in range(self.ledCountY)] for x in range(self.ledCountX)]
        self.lightning = Lightning(self.LIGHTNING_PROBABILITY, self.LIGHTNING_FADE_TIME)

        self._createConfiguration()

    def _createConfiguration(self):
        frequencyItem = NumberItem(self.FREQUENCY_TITLE, self.FREQUENCY_KEY, self.setDropsPerSecond, self.getDropsPerSecond, min=1)
        fallSpeedItem = NumberItem(self.FALL_SPEED_TITLE, self.FALL_SPEED_KEY, self.setFallSpeed, self.getFallSpeed, min=1)
        lightningProbabilityItem = NumberItem(self.LIGHTNING_PROBABILITY_TITLE, self.LIGHTNING_PROBABILITY_KEY,
                                              self.lightning.setProbability, self.lightning.getProbability, min=0, max=1, step=0.01)
        lightningFadeTimeItem = NumberItem(self.LIGHTNING_FADE_TIME_TITLE, self.LIGHTNING_FADE_TIME_KEY,
                                           self.lightning.setFadeTime, self.lightning.getFadeTime, min=0, max=2, step=0.05)
        self.configurer = CustomConfigurer(self, self.NAME, [frequencyItem, fallSpeedItem, lightningProbabilityItem, lightningFadeTimeItem])

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
                for (y, brightness) in drop.calculate().items():
                    if 0 <= y < self.ledCountY and brightness[2] > self.cells[x][y][2]:
                        self.cells[x][y] = brightness

        for __ in range(self.rainDrops.count(None)):
            self.rainDrops.remove(None)

        if (t - self.lastIncrement) >= 1.0 / self.dropsPerSecond:
            x = randint(0, self.ledCountX - 1)
            self.rainDrops.append(RainDrop(x, self.ledCountY + 1, t, self.fallSpeed))
            self.lastIncrement = t

    def _evaluateCell(self, x, y, t):
        colour = self.cells[x][self.ledCountY - (y + 1)]
        flash = self.lightning.getBrightness()
        return int(max(flash, colour[0])), int(max(flash, colour[1])), int(max(flash, colour[2]))

    def reset(self):
        super(StormPixelWriter, self).reset()
        self.lastIncrement = 0
        self.rainDrops = []
        self.lightning.reset()

    def setDropsPerSecond(self, dropsPerSecond):
        self.dropsPerSecond = float(dropsPerSecond)

    def getDropsPerSecond(self):
        return int(round(self.dropsPerSecond))

    def setFallSpeed(self, fallSpeed):
        self.fallSpeed = float(fallSpeed)

    def getFallSpeed(self):
        return self.fallSpeed
