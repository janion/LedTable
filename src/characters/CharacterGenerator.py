
import Image
from scipy.misc import fromimage
import sys


CHARACTERS = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    ".", ",", "!", "?", "/","+", "-", "=", "*", ":", ";", "'", "#", "(", ")"
]
SPECIAL = {
    " ": "space",
    ".": "dot",
    ",": "comma",
    "!": "exclamation",
    "?": "question",
    "/": "fSlash",
    "+": "plus",
    "-": "minus",
    "=": "equals",
    "*": "asterisk",
    ":": "colon",
    ";": "semicolon",
    "'": "apostrophe",
    "#": "hash",
    "(": "openBracket",
    ")": "closeBracket"
}
FILE_TYPE = ".png"
SEPARATOR = "\n"
OUTPUT_FILE_NAME = "characters.py"

FILE_CONTENT = SEPARATOR + "CHARACTERS = {" + SEPARATOR
ENTRY_FORMAT = "    \"%s\": %s,"
FILE_END = "}" + SEPARATOR

def listToString(listToConvert):
    string = "["
    for entry in listToConvert:
        string += str(entry) + ", "
    return string[ : -2] + "]"


if __name__ == "__main__":
    outputFileString = "%s" % FILE_CONTENT
    for char in CHARACTERS:
        fileName = SPECIAL.get(char, char)
        try:
            im = Image.open(fileName + FILE_TYPE)
        except IOError:
            print "File not found: %s" %fileName + FILE_TYPE
            continue
        data = fromimage(im)

        for x in range(im.size[1]):
            for y in range(im.size[0]):
                if data[x, y].tolist() == [0, 0, 0, 255] or data[x, y].tolist() == [0, 0, 0]:
                    sys.stdout.write("@")
                else:
                    sys.stdout.write(".")
            sys.stdout.write(SEPARATOR)

        values = []
        for y in range(im.size[0]):
            value = 0
            for x in range(im.size[1]):
                value <<= 1
                if data[x, y].tolist() == [0, 0, 0, 255] or data[x, y].tolist() == [0, 0, 0]:
                    value += 1
            values.append(value)
        line = ENTRY_FORMAT % (char, listToString(values))
        sys.stdout.write(line + SEPARATOR + SEPARATOR)
        outputFileString += line + SEPARATOR
    outputFileString += FILE_END

    with open(OUTPUT_FILE_NAME, "w") as pyFile:
        pyFile.write(outputFileString)
        print outputFileString
