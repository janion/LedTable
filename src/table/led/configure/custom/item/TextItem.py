from table.led.configure.custom.item.Item import Item


class TextItem(Item):

    TYPE = "text"

    def __init__(self, title, name, setValueAction, getValueAction):
        super(TextItem, self).__init__(self.TYPE, title, name, setValueAction, getValueAction)

    def createFormEntry(self):
        return super(TextItem, self).createFormEntry() % self.EMPTY

if __name__ == "__main__":
    item = TextItem("Pick some text", "text_content", lambda val: None, lambda: "CurrentValue")
    print(item.createFormEntry())
