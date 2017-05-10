import csv

from table.pattern.Pattern import Pattern


class PatternReader(object):

    def readPatterns(self, fileName):
        patterns = []
        with open(fileName) as csvFile:
            reader = csv.reader(csvFile, delimiter=",")
            for row in reader:
                if len(row) == 4:
                    patterns.append(Pattern(row[0], row[1], row[2], row[3]))

        return patterns


class PatternWriter(object):

    def writePatterns(self, fileName, patterns):
        with open(fileName) as csvFile:
            writer = csv.reader(csvFile, delimiter=",")
            for pattern in patterns:
                writer.writerow([pattern.getName(), pattern.getRedFunction(),
                                 pattern.getGreenFunction(), pattern.getBlueFunction()
                                 ])
