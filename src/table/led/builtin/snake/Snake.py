from random import randint
from time import time

UP = "UP"
DOWN = "DOWN"
RIGHT = "RIGHT"
LEFT = "LEFT"


class Snake(object):

    DEFAULT_POSITION = [(0, 0), (0, 1), (0, 2)]

    def __init__(self, snake=None, position=None):
        if position is not None:
            self.position = position
        elif snake is None:
            self.position = [entry for entry in self.DEFAULT_POSITION]
        else:
            self.position = [entry for entry in snake.position]

    def move(self, direction):
        head = self.position[0]
        if direction is UP:
            newHead = (head[0], head[1] + 1)
        elif direction is DOWN:
            newHead = (head[0], head[1] - 1)
        elif direction is RIGHT:
            newHead = (head[0] + 1, head[1])
        elif direction is LEFT:
            newHead = (head[0] - 1, head[1])

        self.position.insert(0, newHead)
        return self.position.pop()

    def extendTail(self, position):
        return self.position.append(position)

    def positionIsOnBody(self, position):
        return position in self.position[1 : ]

    def headIsAt(self, position):
        return self.position[0] == position

    def hasCrashed(self):
        return self.position.count(self.position[0]) > 1

    def hasLeftGrid(self, gridSizeX, gridSizeY):
        head = self.position[0]
        return not ((0 <= head[0] < gridSizeX) and (0 <= head[1] < gridSizeY))


class SnakeCalculator(object):

    def __init__(self, gridSizeX, gridSizeY):
        self.gridSizeX = gridSizeX
        self.gridSizeY = gridSizeY

    def findPath(self, destination, snake=None, direction=None):
        snake = Snake(snake)
        if direction is not None:
            snake.move(direction)
            if snake.hasCrashed() or snake.hasLeftGrid(self.gridSizeX, self.gridSizeY):
                return None

        if snake.headIsAt(destination):
            return []
        else:
            directions = [UP, DOWN, RIGHT, LEFT]
            while len(directions) > 0:
                nextDirection = directions.pop(randint(0, len(directions) - 1))
                result = self.findPath(destination, snake, nextDirection)
                if result is not None:
                    result.insert(0, nextDirection)
                    return result

            return None


# if __name__ == "__main__":
#     position = [(5, 5), (5, 4), (5, 3), (5, 2), (4, 2), (3, 2), (3, 3),
#                 (2, 3), (1, 3), (1, 4), (1, 5), (2, 5), (3, 5)
#                 ]
#     calc = SnakeCalculator(7, 7)
#     result = calc.findPath((2, 2), Snake(position=position))
#     print result
#
#
#     position = [(2, 0), (2, 1), (1, 1), (0, 1), (0, 2), (1, 2)]
#     calc = SnakeCalculator(3, 3)
#     result = calc.findPath((2, 2), Snake(position=position))
#     print result
#
#
#     position = [(1, 0), (2, 0), (2, 1), (1, 1), (0, 1), (0, 2), (1, 2)]
#     calc = SnakeCalculator(3, 3)
#     result = calc.findPath((2, 2), Snake(position=position))
#     print result
#
#
#     #Speed test
#     position = [(5, 5), (5, 4), (5, 3), (5, 2), (4, 2), (3, 2), (3, 3),
#                 (2, 3), (1, 3), (1, 4), (1, 5), (2, 5), (3, 5)
#                 ]
#     calc = SnakeCalculator(10, 10)
#     runs = 1000
#     start = time()
#     for x in range(runs):
#         calc.findPath((2, 2), Snake(position=position))
#     end = time()
#     print (end - start) / runs
