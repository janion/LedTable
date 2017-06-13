from characters.characters import CHARACTERS


class Text(object):

    def __init__(self, gridX, gridY, text):
        self.gridX = gridX
        self.gridY = gridY
        self.text = text
        self.position = 0

        self.columns = [0] * gridX
        for char in text:
            self.columns += CHARACTERS.get(char)
            self.columns += [0]

    def isOnChar(self, x, y):
        column = (x + self.position) % len(self.columns)
        return (self.columns[column] >> (self.gridY - (y + 1))) & 1 == 1

    def move(self):
        self.position = (self.position + 1) % len(self.columns)

    def reset(self):
        self.position = 0

# if __name__ == "__main__":
#     import sys
#     t = Text(10, 10, "1")
#     for x in range(10):
#         t.move()
#     for y in range(10):
#         for x in range(10):
#             if t.isOnChar(x, y):
#                 sys.stdout.write("@")
#             else:
#                 sys.stdout.write(".")
#         sys.stdout.write("\n")