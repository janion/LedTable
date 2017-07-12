

class UrlCorrector(object):
    CORRECTIONS = {"+": " ",
                   "%20": " ",
                   ".": ".",
                   "%2C": ",",
                   "%21": "!",
                   "%3F": "?",
                   "%2F": "/",
                   "%2B": "+",
                   "-": "-",
                   "%3D": "=",
                   "*": "*",
                   "%3A": ":",
                   "%3B": ";",
                   "%27": "'",
                   "%23": "#",
                   "%28": "(",
                   "%29": ")"}

    def correctUrl(self, url):
        newUrl = url
        for (old, new) in self.CORRECTIONS.iteritems():
            newUrl = newUrl.replace(old, new)
        return newUrl


