from random import randint

TUMBLER = [(1, 4), (1, 3), (1, 2), (2, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (2, 7), (2, 6),
           (7, 4), (7, 3), (7, 2), (6, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (6, 7), (6, 6)
           ]
EXPLODER = [(4, 2), (4, 6),
            (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
            (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)
            ]
R_PENTOMINO = [(5, 3), (5, 4), (5, 5), (6, 5), (4, 4)]
DIE_HARD = [(1, 5), (2, 5), (2, 4), (6, 4), (7, 4), (8, 4), (7, 6)]

class GameOfLife(object):

    def __init__(self, gridSizeX, gridSizeY):
        self.gridSizeX = gridSizeX
        self.gridSizeY = gridSizeY
        self.data = [[0 for y in range(gridSizeY)] for x in range(gridSizeX)]

    def setStartCondition(self, positions):
        for pos in positions:
            self.data[pos[0]][pos[1]] = 1

    def setRandomStartCondition(self):
        for x in range((self.gridSizeX * self.gridSizeY) / 2):
            self.data[randint(0, self.gridSizeX - 1)][randint(0, self.gridSizeY - 1)] = 1

    def isPopulated(self, x, y):
        return self.data[x][y] == 1

    def tick(self):
        newData = [[0 for y in range(self.gridSizeY)] for x in range(self.gridSizeX)]

        for x in range(self.gridSizeX):
            for y in range(self.gridSizeY):
                if self.populatedNextTick(x, y):
                    newData[x][y] = 1
                else:
                    newData[x][y] = 0

        self.data = newData

    def populatedNextTick(self, x, y):
        neighbours = self.getNeighbourCount(x, y)
        if self.data[x][y] == 1:
            if neighbours == 2 or neighbours == 3:
                return True
            else:
                return False
        else:
            return neighbours == 3

    def getNeighbourCount(self, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                indexX = x + i
                indexY = y + j
                if 0 <= indexX < self.gridSizeX and 0 <= indexY < self.gridSizeY:
                    if self.data[indexX][indexY] == 1:
                        count += 1
        return count

if __name__ == "__main__":
    gameOfLife = GameOfLife(10, 10)
    gameOfLife.setStartCondition([(4, 0), (4, 1), (4, 2), (4, 3), (4, 4),
                                  (4, 5), (4, 6), (4, 7), (4, 8), (4, 9)
                                  ])
    print gameOfLife.getNeighbourCount(0, 0)
    print gameOfLife.getNeighbourCount(4, 1)
    print gameOfLife.getNeighbourCount(5, 1)
    gameOfLife.tick()
