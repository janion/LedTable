

class ColourConverter(object):

    HASH = "#"
    CHARACTERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]

    def convertFromHtmlToColour(self, colourString):
        red = colourString[1: 3]
        green = colourString[3: 5]
        blue = colourString[5: 7]
        return self._convertByteCodeToNumber(red),  self._convertByteCodeToNumber(green),  self._convertByteCodeToNumber(blue)

    def _convertByteCodeToNumber(self, byteString):
        return (self.CHARACTERS.index(byteString[0]) * 16) + self.CHARACTERS.index(byteString[1])

    def convertFromColourToHtml(self, colour):
        red = colour[0]
        green = colour[1]
        blue = colour[2]
        return self.HASH + self._convertNumberToByteCode(red) +  self._convertNumberToByteCode(green) +  self._convertNumberToByteCode(blue)

    def _convertNumberToByteCode(self, colourValue):
        return self.CHARACTERS[int(colourValue / 16)] + self.CHARACTERS[colourValue % 16]

if __name__ == "__main__":
    print(ColourConverter().convertFromHtmlToColour("#ff00fe"))
    print(ColourConverter().convertFromHtmlToColour("#501012"))
    print(ColourConverter().convertFromColourToHtml((255, 0, 254)))
    print(ColourConverter().convertFromColourToHtml((80, 16, 18)))

    print(ColourConverter().convertFromHtmlToColour(ColourConverter().convertFromColourToHtml((255, 0, 254))))
    print(ColourConverter().convertFromColourToHtml(ColourConverter().convertFromHtmlToColour("#ff00fe")))
