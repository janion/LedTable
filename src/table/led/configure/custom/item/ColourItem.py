from table.led.configure.custom.item.Item import Item


class ColourItem(Item):

    TYPE = "color"

    def __init__(self, title, name, setValueAction, getValueAction):
        super(ColourItem, self).__init__(self.TYPE, title, name, setValueAction, getValueAction)

    def createFormEntry(self):
        return super(ColourItem, self).createFormEntry() % self.EMPTY

if __name__ == "__main__":
    item = ColourItem("Pick a colour", "my_colour", lambda val: None, lambda: "#ff003b")
    print item.createFormEntry()
