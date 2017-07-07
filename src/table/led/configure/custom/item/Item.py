

class Item(object):

    EMPTY = ""
    EMPTY_FORMAT = "%s"
    FORM_FORMAT = "%s<br>\n<input type=\"%s\" name=\"%s\" value=\"%s\"%s><br>"
    EXTRA_FORMAT = " %s=\"%s\""

    def __init__(self, type, title, name, setValueAction, getValueAction):
        self.type = type
        self.title = title
        self.name = name
        self.setValueAction = setValueAction
        self.getValueAction = getValueAction

    def createFormEntry(self):
        return self.FORM_FORMAT % (self.title, self.type, self.name, str(self.getValueAction()), self.EMPTY_FORMAT)

    def getKey(self):
        return self.name

    def setValue(self, value):
        self.setValueAction(value)
