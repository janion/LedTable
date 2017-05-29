from random import randint

UP = "UP"
DOWN = "DOWN"
RIGHT = "RIGHT"
LEFT = "LEFT"
DIRECTIONS = [UP, DOWN, RIGHT, LEFT]


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

    def distanceTo(self, position):
        head = self.position[0]
        return abs(head[0] - position[0]) + abs(head[1] - position[1])


class SnakeRandomCalculator(object):

    def __init__(self, gridSizeX, gridSizeY):
        self.gridSizeX = gridSizeX
        self.gridSizeY = gridSizeY

    def findPath(self, destination, snake, direction=None):
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


class SnakeDirectionCalculator(object):

    def orderDirections(self, snake, destination):
        distances = []
        for direction in DIRECTIONS:
            tmpSnake = Snake(snake)
            tmpSnake.move(direction)
            distance = tmpSnake.distanceTo(destination)
            isPlaced = False
            for x in range(len(distances)):
                if distance < distances[x][0]:
                    distances.insert(x, (distance, direction))
                    isPlaced = True
                    break
            if not isPlaced:
                distances.append((distance, direction))

        return [entry[1] for entry in distances]


class SnakeInformedCalculator(object):

    def __init__(self, gridSizeX, gridSizeY):
        self.gridSizeX = gridSizeX
        self.gridSizeY = gridSizeY
        self.directionCalculator = SnakeDirectionCalculator()

    def findPath(self, destination, snake, direction=None):
        snake = Snake(snake)
        if direction is not None:
            snake.move(direction)
            if snake.hasCrashed() or snake.hasLeftGrid(self.gridSizeX, self.gridSizeY):
                return None

        if snake.headIsAt(destination):
            return []
        else:
            for direction in self.directionCalculator.orderDirections(snake, destination):
                result = self.findPath(destination, snake, direction)
                if result is not None:
                    result.insert(0, direction)
                    return result

            return None


class SnakePanicCalculator(object):

    def __init__(self, gridSizeX, gridSizeY):
        self.gridSizeX = gridSizeX
        self.gridSizeY = gridSizeY
        self.directionCalculator = SnakeDirectionCalculator()

    def findPath(self, snake, direction=None, directions=None, best=None):
        isTop = direction is None
        if direction is None:
            best = []
        if directions is None:
            directions = []

        snake = Snake(snake)
        if direction is not None:
            snake.move(direction)
            if snake.hasCrashed() or snake.hasLeftGrid(self.gridSizeX, self.gridSizeY):
                return
            elif len(directions) >= len(best):
                while len(best) > 0:
                    best.pop()
                for eachDirection in directions:
                    best.append(eachDirection)

        for newDirection in DIRECTIONS:
            newDirections = [entry for entry in directions]
            newDirections.append(newDirection)
            self.findPath(snake, newDirection, newDirections, best)

        if not isTop:
            return
        else:
            return best
