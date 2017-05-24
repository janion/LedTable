

class ColourWheel(object):

    RED = 0
    GREEN = 120
    BLUE = 240
    CONVERSION = 1.0 / 120

    def getColour(self, intensity, angle):
        angle %= 360
        if angle < 120:
            # Red -> yellow -> green
            r = intensity * ((120 - angle) * self.CONVERSION)
            g = intensity * (angle * self.CONVERSION)
            b = 0
        elif angle < 240:
            # Green -> cyan -> blue
            angle = angle - 120
            r = 0
            g = intensity * ((120 - angle) * self.CONVERSION)
            b = intensity * (angle * self.CONVERSION)
        else:
            # Blue -> magenta -> red
            angle = angle - 240
            r = intensity * (angle * self.CONVERSION)
            g = 0
            b = intensity * ((120 - angle) * self.CONVERSION)

        return int(r), int(g), int(b)
