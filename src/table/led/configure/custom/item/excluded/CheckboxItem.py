from table.led.configure.custom.item.Item import Item


class CheckboxItem(Item):

    TYPE = "checkbox"

    def __init__(self, title, name, setValueAction, getValueAction):
        super(CheckboxItem, self).__init__(self.TYPE, title, name, setValueAction, getValueAction)
        raise NotImplementedError("Does not fit the framework")

    def createFormEntry(self):
        return super(CheckboxItem, self).createFormEntry() % self.EMPTY

if __name__ == "__main__":
    item = CheckboxItem("Is ticked", "tick_check", lambda val: None, lambda: True)
    print item.createFormEntry()
