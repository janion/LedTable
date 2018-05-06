

class SelectItem(object):

    HTML_FORMAT = "<select name=\"%s\">\n%s\n</select>"
    ROW_FORMAT = "    <option value=\"%s\"%s>%s</option>"
    EMPTY = ""
    SELECTED = " selected"

    def __init__(self, title, name, setValueAction, getValueAction, optionNames, optionValues):
        self.title = title
        self.name = name
        self.setValueAction = setValueAction
        self.getValueAction = getValueAction
        self.optionNames = optionNames
        self.optionValues = optionValues

    def createFormEntry(self):
        return self.HTML_FORMAT %(self.name, self._createOptions())

    def _createOptions(self):
        options = []
        for (name, value) in zip(self.optionNames, self.optionValues):
            selected = self.SELECTED if value == self.getValueAction() else self.EMPTY
            options.append(self.ROW_FORMAT % (name, selected, value))

        return "\n".join(options)


if __name__ == "__main__":
    names = ["option1", "option2", "option3"]
    values = ["Option 1", "Option 2", "Option 3"]
    item = SelectItem("Pick some text", "text_content", lambda val: None, lambda: "Option 2", names, values)
    print(item.createFormEntry())
