import re as regex

from table.web.UrlCorrector import UrlCorrector


class UrlParser(object):

    def __init__(self):
        self.corrector = UrlCorrector()

    def parseURL(self, url):
        # PARSE THE URL AND RETURN THE PATH AND GET PARAMETERS
        parameters = {}
        path = regex.search("(.*?)(\?|$)", url)

        while True:
            varrs = regex.search("(([a-zA-Z0-9]+)=([a-zA-Z0-9.+%\-]*))&?", url)
            if varrs:
                parameters[varrs.group(2)] = self.corrector.correctUrl(varrs.group(3))
                url = url.replace(varrs.group(0), '')
            else:
                break

        return path.group(1), parameters


if __name__ == "__main__":
    url = """GET /configure?name=patternName&text=hello+my+good+friend%21%3F HTTP/1.0
From: someuser@jmarshall.com
User-Agent: HTTPTool/1.0"""
    corrector = UrlCorrector()
    oldUrl = url

    parameters = {}

    while True:
        varrs = regex.search("(([a-zA-Z0-9]+)=([a-zA-Z0-9.+%]*))&?", url)
        if varrs:
            parameters[varrs.group(2)] = corrector.correctUrl(varrs.group(3))
            url = url.replace(varrs.group(0), '')
        else:
            break

    print(oldUrl)
    print()
    print(("Name =", parameters.get("name")))
    print(("Text =", parameters.get("text")))
