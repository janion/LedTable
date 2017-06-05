import ure as regex


class UrlParser(object):

    def parseURL(self, url):
        # PARSE THE URL AND RETURN THE PATH AND GET PARAMETERS
        parameters = {}

        # Adjust for characters converted for the url
        url = url.replace('%28', '(').replace('%29', ')').replace('+', ' ').replace('%2B', '+').replace('%2F', '-').replace('%20', ' ')
        path = regex.search("(.*?)(\?|$)", url)

        while True:
            varrs = regex.search("(([a-zA-Z0-9]+)=([ a-zA-Z0-8.()\-\+\*\/]*))&?", url)
            if varrs:
                parameters[varrs.group(2)] = varrs.group(3)
                url = url.replace(varrs.group(0), '')
            else:
                break

        return path.group(1), parameters