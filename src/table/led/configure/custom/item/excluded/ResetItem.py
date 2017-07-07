from table.led.configure.custom.item.Item import Item


class ResetItem(Item):

    TYPE = "reset"

    def __init__(self, title, name):
        super(ResetItem, self).__init__(self.TYPE, title, name, None, None)
        raise NotImplementedError("Does not fit the framework")

    def createFormEntry(self):
        return super(ResetItem, self).createFormEntry() % self.EMPTY

if __name__ == "__main__":
    item = ResetItem("Pick some text", "text_content")
    print item.createFormEntry()
