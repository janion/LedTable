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
    request = "/test?Gibbon=True&bold=adol"
    print(request)
    path, parameters = UrlParser().parseURL(request)
    print(path)
    print(parameters)
