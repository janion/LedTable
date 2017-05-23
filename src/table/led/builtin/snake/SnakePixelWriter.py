from table.led.PixelWriter import PixelWriter2D
from table.led.builtin.snake.Snake import Snake, SnakeCalculator
from random import randint


class PixelWriter(PixelWriter2D):

    START_TIME = 0.6
    TIME_DECREASE = 0.02
    HEAD_COLOUR = (255, 0, 0)
    BODY_COLOUR = (0, 255, 0)
    FOOD_COLOUR = (127, 127, 0)
    BACKGROUND_COLOUR = (0, 0, 0)

    def __init__(self, ledCountX, ledCountY, mode):
        super(PixelWriter, self).__init__(ledCountX, ledCountY, None, mode)
        self.startTime = None
        self.lastIncrement = None
        self.timeTick = self.START_TIME

        self.food = (randint(0, ledCountX - 1), randint(0, ledCountY - 1))
        self.snake = Snake()
        self.snakeCalculator = SnakeCalculator(ledCountX, ledCountY)
        self.directions = self.snakeCalculator.findPath(self.food, self.snake)

    def _tick(self, t):
        if self.startTime is None:
            self.startTime = t
            self.lastIncrement = t

        if (t - self.lastIncrement) >= self.timeTick:
            self.lastIncrement = t
            tail = self.snake.move(self.directions.pop(0))
            if self.snake.headIsAt(self.food):
                self.snake.extendTail(tail)
                self.food = (randint(0, self.ledCountX - 1), randint(0, self.ledCountY - 1))
                self.directions = self.snakeCalculator.findPath(self.food, self.snake)
                self.timeTick -= self.TIME_DECREASE

    def _evaluateCell(self, x, y, t):
        position = (x, y)
        if self.snake.positionIsOnBody(position):
            return self.BODY_COLOUR
        elif self.snake.headIsAt(position):
            return self.HEAD_COLOUR
        elif self.food == position:
            return self.FOOD_COLOUR
        else:
            return self.BACKGROUND_COLOUR
