from table.Constants import LED_COUNT_Y
if LED_COUNT_Y == 10:
    from characters.characters10 import CHARACTERS
elif LED_COUNT_Y == 15:
    from characters.characters15 import CHARACTERS


class Text(object):

    def __init__(self, gridX, gridY, text):
        self.gridX = gridX
        self.gridY = gridY
        self.text = text
        self.position = 0

        self.columns = [0]
        self.setTextContent(text)

    def isOnChar(self, x, y):
        column = (x + self.position) % len(self.columns)
        return (self.columns[column] >> (self.gridY - (y + 1))) & 1 == 1

    def move(self):
        self.position = (self.position + 1) % len(self.columns)

    def reset(self):
        self.position = 0

    def setTextContent(self, text):
        self.text = text
        self.columns = [0] * self.gridX
        for char in text:
            self.columns += CHARACTERS.get(char)
            self.columns += [0]
        self.reset()

    def getTextContent(self):
        return self.text
