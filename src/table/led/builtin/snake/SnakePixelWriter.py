from table.led.PixelWriter import PixelWriter2D
from table.led.builtin.snake.Snake import Snake, SnakeInformedCalculator, SnakePanicCalculator
from table.led.ColourWheel import ColourWheel
from random import randint


class PixelWriter(PixelWriter2D):

    START_TIME = 0.6
    TIME_DECREASE = 0.02
    COLOUR_ANGLE_CHANGE = 2
    HEAD_COLOUR = (255, 0, 0)
    BODY_COLOUR = (0, 255, 0)
    FOOD_COLOUR = (127, 127, 0)
    BACKGROUND_COLOUR = (0, 0, 0)

    def __init__(self, ledCountX, ledCountY, mode):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)
        self.colourWheel = ColourWheel()
        self.startTime = None
        self.lastIncrement = None
        self.timeTick = self.START_TIME

        self.snake = Snake()
        self.food = (0, 0)
        self.newFood()
        # self.snakeCalculator = SnakeRandomCalculator(ledCountX, ledCountY)
        self.snakeCalculator = SnakeInformedCalculator(ledCountX, ledCountY)
        self.panicCalculator = SnakePanicCalculator(ledCountX, ledCountY)
        self.directions = self.snakeCalculator.findPath(self.food, self.snake)

        self.isPanic = False

    def _tick(self, t):
        if self.startTime is None:
            self.startTime = t
            self.lastIncrement = t

        if (t - self.lastIncrement) >= self.timeTick:
            self.lastIncrement = t
            tail = self.snake.move(self.directions.pop(0))
            if self.snake.headIsAt(self.food):
                self.snake.extendTail(tail)
                self.newFood()
                self.timeTick -= self.TIME_DECREASE
                self.directions = self.snakeCalculator.findPath(self.food, self.snake)

                if self.directions is None:
                    self.directions = self.panicCalculator.findPath(self.snake)
            if len(self.directions) == 0:
                self.hasLost()

    def newFood(self):
        while self.snake.positionIsOnBody(self.food) or self.snake.headIsAt(self.food):
            self.food = (randint(0, self.ledCountX - 1), randint(0, self.ledCountY - 1))

    def hasLost(self):
        self.timeTick = self.START_TIME
        self.snake = Snake()
        self.directions = self.snakeCalculator.findPath(self.food, self.snake)

    def _evaluateCell(self, x, y, t):
        position = (x, y)
        if self.snake.positionIsOnBody(position):
            # return self.BODY_COLOUR
            return self.colourWheel.getColour(
                255, ColourWheel.GREEN + (self.snake.position.index(position) * self.COLOUR_ANGLE_CHANGE)
                )
        elif self.snake.headIsAt(position):
            return self.HEAD_COLOUR
        elif self.food == position:
            return self.FOOD_COLOUR
        else:
            return self.BACKGROUND_COLOUR
